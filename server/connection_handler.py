from __future__ import annotations

import selectors
import json
import io
import struct
import sys
import socket
import pickle
import logging
logger = logging.getLogger("EWlogger")

"""
TConnectionHandler handles communication between client and server
"""
class TConnectionHandler:
	_buffer: bytes = b"" # Buffer for received/sent bytes
	selector: selectors.BaseSelector
#	sock: socket.socket
	addr: str
	request: dict
	_jsonheader_len: int = -1
	jsonheader: dict | None = None

	"""
	Initialize the communicator
	"""
	def __init__(self, selector: selectors.BaseSelector, sock: socket.socket, addr: str):
		logger.debug(f"{__class__.__name__}->__init__( selector, sock, addr )")
		self.selector = selector
		self.sock: socket.socket = sock
		self.addr = addr
		self.request = {}

	def _set_selector_events_mask(self, mode: str):
		logger.debug(f"{__class__.__name__}->_set_selector_events_mask( {mode} )")
		"""Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
		if mode == "r":
			events = selectors.EVENT_READ
		elif mode == "w":
			events = selectors.EVENT_WRITE
		else:
			events = selectors.EVENT_READ | selectors.EVENT_WRITE
		self.selector.modify(self.sock, events, data=self)
	
	def prepare_response(self, request: dict):
		logger.debug(f"{__class__.__name__}->prepare_response( request )")
#		logger.debug(request)
		self.request = request
		self.jsonheader = {"content-type": "binary/binary"}
		self.create_response()
		self._set_selector_events_mask("w")

	"""
	Dispatch the message
	"""
	def dispatch(self, mask: int) -> bool:
		logger.debug(f"{__class__.__name__}->dispatch( {mask} )")
		if mask == selectors.EVENT_READ:
			return self.rx_dispatch()
		else:
			return self.tx_dispatch()

	"""
	Close down the communication with the client
	"""
	def close(self):
		logger.debug(f"{__class__.__name__}->close()")
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
			del(self.sock)

	"""
	Read bytes from the connection into the buffer
	"""
	def _read(self):
		logger.debug(f"{__class__.__name__}->_read()")
		try:
			data = self.sock.recv(8192)
		except BlockingIOError:
			# Ignore that resource temporarily unavailable (errno EWOULDBLOCK)
			pass
		else:
			if data:
				self._buffer += data
			else:
				logger.warning(f"{__class__.__name__} peer closed.")
				exit()

	"""
	Transform JSON into data using the specified encoding
	"""
	def _json_decode(self, json_bytes: bytes, encoding: str):
		logger.debug(f"{__class__.__name__}->_json_decode( json_bytes, encoding )")
		tiow = io.TextIOWrapper(
			io.BytesIO(json_bytes), encoding=encoding, newline=""
		)
		obj = json.load(tiow)
		tiow.close()
		return obj

	"""
	Process the request when fully received
	"""
	def process_request(self) -> bool:
		logger.debug(f"{__class__.__name__}->process_request()")
		content_len = 0
		if self.jsonheader is not None:
			content_len = self.jsonheader["content-length"]
		if len(self._buffer) < content_len:
			return False # Content not received in full yet, stop processing

		# Content received, process
		data = self._buffer[:content_len]
		self._buffer = self._buffer[content_len:]
		if self.jsonheader is not None:
			if self.jsonheader["content-type"] == "text/json":
				encoding = self.jsonheader["content-encoding"]
				self.request = self._json_decode(data, encoding)
				logger.debug(f"- request is {self.request}")
			else:
				# Extract the request from the content
				self.request = pickle.loads(data)
				logger.debug(f"- request is {self.request}")
		return True

	"""
	Process the json header when fully received
	"""
	def process_jsonheader(self):
		logger.debug(f"{__class__.__name__}->process_jsonheader()")
		hdrlen = self._jsonheader_len
		if len(self._buffer) < hdrlen:
			return None # Header not received in full yet, stop processing

		# Header received, process		
		self.jsonheader = self._json_decode(self._buffer[:hdrlen], "utf-8")
		self._buffer = self._buffer[hdrlen:]
		if self.jsonheader is not None:
			for reqhdr in ("byteorder", "content-length", "content-type", "content-encoding",):
				if reqhdr not in self.jsonheader:
					logger.warning(f"Missing required header '{reqhdr}'.")

	"""
	Process the protoheader when fully received
	"""
	def process_protoheader(self):
		logger.debug(f"{__class__.__name__}->process_protoheader()")
		logger.debug(f"- buffer len {len(self._buffer)}")
		hdrlen = 2
		if len(self._buffer) < hdrlen:
			return None # Protoheader not received in full yet, stop processing

		logger.debug("- protoheader received, process")
		self._jsonheader_len = struct.unpack(">H", self._buffer[:hdrlen])[0]
		self._buffer = self._buffer[hdrlen:]

	"""
	Dispatch the message event
	Read a message from the client till the full message has been received
	The message is read in several parts - the protoheader, the jsonheader, and the content
	"""
	def rx_dispatch(self) -> bool:
		logger.debug(f"{__class__.__name__}->rx_dispatch()")
		self._read()
		logger.debug(f"- checking jsonheader {self._jsonheader_len}")
		if self._jsonheader_len < 0:
			self.process_protoheader()
		logger.debug(f"- checking jsonheader {self._jsonheader_len}")
		if self._jsonheader_len >= 0:
			if self.jsonheader is None:
				self.process_jsonheader()
		logger.debug(f"- checking jsonheader {self.jsonheader}")
		if self.jsonheader:
			logger.debug(f"- checking request {self.request}")
			print(f"{self.request.__getstate__()}")
			if self.request == {}:
				return self.process_request()
		return False

	"""
	Write bytes to the connection from the buffer
	"""
	def _write(self) -> bool:
		blen = len(self._buffer)
		logger.debug(f"{__class__.__name__}->_write( {blen} bytes)")
		if self._buffer:
			try:
				sent = self.sock.send(self._buffer)
			except BlockingIOError:
				# Ignore that resource temporarily unavailable (errno EWOULDBLOCK)
				pass
			else:
				self._buffer = self._buffer[sent:]
				# Close when the buffer is drained. The response has been sent.
				if sent and not self._buffer:
#					self.close()
					return True
		return False

	"""
	Transform data into JSON using the specified encoding
	"""
	def _json_encode(self, data: dict, encoding: str):
		logger.debug(f"{__class__.__name__}->_json_encode( data, encoding )")
		return json.dumps(data, ensure_ascii=False).encode(encoding)

	"""
	Construct a message from the specified data elements
	"""
	def _create_message(self, *, content_bytes: bytes, content_type: str, content_encoding: str):
		logger.debug(f"{__class__.__name__}->_create_message( *, content_bytes, content_type, content_encoding )")
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

	"""
	Generate a json message
	"""
	def _create_response_json_content(self):
		logger.debug(f"{__class__.__name__}->_create_response_json_content()")
		content_encoding = "utf-8"
		response = {
			"content_bytes": self._json_encode(self.request, content_encoding),
			"content_type": "text/json",
			"content_encoding": content_encoding,
		}
		return response

	"""
	Generate a binary message
	"""
	def _create_response_binary_content(self):
		logger.debug(f"{__class__.__name__}->_create_response_binary_content()")
		response = {
			"content_bytes": pickle.dumps(self.request),
			"content_type": "binary/custom-server-binary-type",
			"content_encoding": "binary",
		}
		return response

	"""
	Generate the message
	"""
	def create_response(self):
		logger.debug(f"{__class__.__name__}->create_response()")

		if self.jsonheader is not None:
			if self.jsonheader["content-type"] == "text/json":
				response = self._create_response_json_content()
			else:
				response = self._create_response_binary_content()

		message = self._create_message(**response)
		self.response_created = True
		self._buffer = message

	"""
	Dispatch the message event
	"""
	def tx_dispatch(self) -> bool:
		logger.debug(f"{__class__.__name__}->dispatch( mask )")
		return self._write()
