from typing import Optional
import uuid
import selectors
import json
import io
import struct
import sys
import lzma
import pickle
import logging
import random
logger = logging.getLogger("EWlogger")

from worlds import TWorld

class TMessage:
	def __init__(self, selector, sock, addr, world: TWorld):
		logger.debug(f"TMessage->__init__( selector, sock, addr, world )")
		self.selector: selectors.DefaultSelector = selector
		self.sock = sock
		self.addr = addr
		self.world: TWorld = world
		self._recv_buffer = b""
		self._send_buffer = b""
		self._jsonheader_len = None
		self.jsonheader = None
		self.request = None
		self.response_created = False
		self.map = None

	""" Switch to the specified mode """
	def _set_selector_events_mask(self, mode):
		logger.debug("TMessage->_set_selector_events_mask( mode )")
		if mode == "r":
			events = selectors.EVENT_READ
		elif mode == "w":
			events = selectors.EVENT_WRITE
		elif mode == "rw":
			events = selectors.EVENT_READ | selectors.EVENT_WRITE
		else:
			logger.error(f"Invalid events mask mode {mode!r}.")
		self.selector.modify(self.sock, events, data=self)

	""" Read bytes from the connection into the receive buffer """
	def _read(self):
		logger.debug("TMessage->_read()")
		try:
			data = self.sock.recv(4096)
		except BlockingIOError:
			# Ignore that resource temporarily unavailable (errno EWOULDBLOCK)
			pass
		else:
			if data:
				self._recv_buffer += data
			else:
				logger.warning("Peer closed.")

	""" Write bytes to the connection from the send buffer """
	def _write(self):
		logger.debug("TMessage->_write()")
		if self._send_buffer:
			try:
				sent = self.sock.send(self._send_buffer)
			except BlockingIOError:
				# Ignore that resource temporarily unavailable (errno EWOULDBLOCK)
				pass
			else:
				self._send_buffer = self._send_buffer[sent:]
				# Close when the buffer is drained. The response has been sent.
				if sent and not self._send_buffer:
					self.close()

	""" Transform data into JSON using the specified encoding """
	def _json_encode(self, data, encoding):
		logger.debug("TMessage->_json_encode( data, encoding )")
		return json.dumps(data, ensure_ascii=False).encode(encoding)

	""" Transform JSON into data using the specified encoding """
	def _json_decode(self, json_bytes, encoding):
		logger.debug("TMessage->_json_decode( json_bytes, encoding )")
		tiow = io.TextIOWrapper(
			io.BytesIO(json_bytes), encoding=encoding, newline=""
		)
		obj = json.load(tiow)
		tiow.close()
		return obj

	""" Construct a message from the specified data elements """
	def _create_message(self, *, content_bytes, content_type, content_encoding):
		logger.debug("TMessage->_create_message( *, content_bytes, content_type, content_encoding )")
		jsonheader = {
			"byteorder": sys.byteorder,
			"content-type": content_type,
			"content-encoding": content_encoding,
			"content-length": len(content_bytes),
		}
		jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
		message_hdr = struct.pack(">H", len(jsonheader_bytes))
		message = message_hdr + jsonheader_bytes + content_bytes
		return message

	""" Construct response content """
	def _create_response_json_content(self):
		logger.debug("TMessage->_create_response_json_content()")
		content_encoding = "utf-8"
		response = {
			"content_bytes": self._json_encode(self.request, content_encoding),
			"content_type": "text/json",
			"content_encoding": content_encoding,
		}
		return response

	def _create_response_binary_content(self):
		logger.debug("TMessage->_create_response_binary_content()")
		response = {
			"content_bytes": pickle.dumps(self.request),
			"content_type": "binary/custom-server-binary-type",
			"content_encoding": "binary",
		}
		return response

	""" Dispatch the message event """
	def dispatch(self, mask) -> bool:
		logger.debug("TMessage->dispatch( mask )")
		if mask & selectors.EVENT_READ:
			return self.read()
		if mask & selectors.EVENT_WRITE:
			return self.write()

	"""
	Read a message from the client till the full message has been received
	The message is read in several parts - the protoheader, the jsonheader, and the content
	"""
	def read(self) -> bool:
		logger.debug("TMessage->read()")
		self._read()

		if self._jsonheader_len is None:
			self.process_protoheader()

		if self._jsonheader_len is not None:
			if self.jsonheader is None:
				self.process_jsonheader()

		if self.jsonheader:
			if self.request is None:
				return self.process_request()
		return False

	""" Write a message to the client till the full message has been sent """
	def write(self) -> bool:
		logger.debug("TMessage->write()")
		if self.request:
			if not self.response_created:
				self.create_response()
		return self._write()

	def close(self):
		logger.debug("TMessage->close()")
		try:
			self.selector.unregister(self.sock)
		except Exception as e:
			logger.warning(
				f"Error: selector.unregister() exception for "
				f"{self.addr}: {str(e)}"
			)

		try:
			self.sock.close()
		except OSError as e:
			logger.warning(f"Error: socket.close() exception for {self.addr}: {str(e)}")
		finally:
			# Delete reference to socket object for garbage collection
			self.sock = None

	def process_protoheader(self):
		logger.debug("TMessage->process_protoheader()")
		hdrlen = 2
		if len(self._recv_buffer) < hdrlen:
			return None # Protoheader not received in full yet, stop processing

		# Protoheader received, process		
		self._jsonheader_len = struct.unpack(">H", self._recv_buffer[:hdrlen])[0]
		self._recv_buffer = self._recv_buffer[hdrlen:]

	def process_jsonheader(self):
		logger.debug("TMessage->process_jsonheader()")
		hdrlen = self._jsonheader_len
		if len(self._recv_buffer) < hdrlen:
			return None # Header not received in full yet, stop processing

		# Header received, process		
		self.jsonheader = self._json_decode(self._recv_buffer[:hdrlen], "utf-8")
		self._recv_buffer = self._recv_buffer[hdrlen:]
		for reqhdr in ("byteorder", "content-length", "content-type", "content-encoding",):
			if reqhdr not in self.jsonheader:
				logger.warning(f"Missing required header '{reqhdr}'.")

	def process_request(self) -> bool:
		logger.debug("TMessage->process_request()")
		content_len = self.jsonheader["content-length"]
		if len(self._recv_buffer) < content_len:
			return False # Content not received in full yet, stop processing

		# Content received, process
		self.request = {
			"cmd": "nop"
		}
		data = self._recv_buffer[:content_len]
		self._recv_buffer = self._recv_buffer[content_len:]
		if self.jsonheader["content-type"] == "text/json":
			encoding = self.jsonheader["content-encoding"]
			request: dict = self._json_decode(data, encoding)
		else:
			# Extract the request from the content
			request = pickle.loads(data)
#		return True

		request_cmd = request.get("cmd")
		if request_cmd == "new":
			# Gather the NEW GAME information and return it
			cid = f"CID#{uuid.uuid4()}"
#			self.world.add_actor(cid, self.addr)

			self.request = {
				"cmd": request_cmd,
				"cid": cid,
				"name": self.world.name,
				"entry_point": self.world.entry_point(), # One entry point of the world
				"map_sizes" : self.world.map_definitions(), # All map sizes to ensure the client is prepared
			}
		elif request_cmd == "fos":
			# Gather the FOS view and return it
			self.request = {
				"cmd": request_cmd,
				"fos": self.world.field_of_sense(fos_request=request),
			}
		# Set selector to listen for write events, we're done reading.
		self._set_selector_events_mask("w")

	def create_response(self):
		logger.debug("TMessage->create_response()")

		if self.jsonheader["content-type"] == "text/json":
			response = self._create_response_json_content()
		else:
			response = self._create_response_binary_content()

		message = self._create_message(**response)
		self.response_created = True
		self._send_buffer += message
