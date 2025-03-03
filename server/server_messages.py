"""
Class TMessage
	__init__( selector, sock, addr, world )
	_set_selector_events_mask( mode )
	_read()
	_write()
	_json_encode( data, encoding )
	_json_decode( json_bytes, encoding )
	_create_message( *, content_bytes, content_type, content_encoding )
	_create_response_json_content()
	_create_response_binary_content()
	dispatch( mask )
	read()
	write()
	close()
	process_protoheader()
	process_jsonheader()
	process_request() -> Optional( dict)
	create_response()

"""
from typing import Optional
import selectors
import json
import io
import struct
import sys

#import tile_types

from worlds import TWorld

class TMessage:
	def __init__(self, selector, sock, addr, world: TWorld):
		print("TMessageHandler->__init__( selector, sock, addr, world )")
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
		print("TMessageHandler->_set_selector_events_mask( mode )")
		if mode == "r":
			events = selectors.EVENT_READ
		elif mode == "w":
			events = selectors.EVENT_WRITE
		elif mode == "rw":
			events = selectors.EVENT_READ | selectors.EVENT_WRITE
		else:
			raise ValueError(f"Invalid events mask mode {mode!r}.")
		self.selector.modify(self.sock, events, data=self)

	""" Read bytes from the connection into the receive buffer """
	def _read(self):
		print("TMessageHandler->_read()")
		try:
			data = self.sock.recv(4096)
		except BlockingIOError:
			# Ignore that resource temporarily unavailable (errno EWOULDBLOCK)
			pass
		else:
			if data:
				self._recv_buffer += data
			else:
				raise RuntimeError("Peer closed.")

	""" Write bytes to the connection from the send buffer """
	def _write(self):
		print("TMessageHandler->_write()")
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
		print("TMessageHandler->_json_encode( data, encoding )")
		return json.dumps(data, ensure_ascii=False).encode(encoding)

	""" Transform JSON into data using the specified encoding """
	def _json_decode(self, json_bytes, encoding):
		print("TMessageHandler->_json_decode( json_bytes, encoding )")
		tiow = io.TextIOWrapper(
			io.BytesIO(json_bytes), encoding=encoding, newline=""
		)
		obj = json.load(tiow)
		tiow.close()
		return obj

	""" Construct a message from the specified data elements """
	def _create_message(
		self, *, content_bytes, content_type, content_encoding
	):
		print("TMessageHandler->_create_message( *, content_bytes, content_type, content_encoding )")
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
		print("TMessageHandler->_create_response_json_content()")
		content_encoding = "utf-8"
		response = {
			"content_bytes": self._json_encode(self.request, content_encoding),
			"content_type": "text/json",
			"content_encoding": content_encoding,
		}
		return response

	def _create_response_binary_content(self):
		print("TMessageHandler->_create_response_binary_content()")
		response = {
			"content_bytes": self.request,
			"content_type": "binary/custom-server-binary-type",
			"content_encoding": "binary",
		}
		return response

	""" Dispatch the message event """
	def dispatch(self, mask):
		print("TMessageHandler->dispatch( mask )")
		if mask & selectors.EVENT_READ:
			self.read()
		if mask & selectors.EVENT_WRITE:
			self.write()

	"""
	Read a message from the client till the full message has been received
	The message is read in several parts - the protoheader, the jsonheader, and the content
	"""
	def read(self):
		print("TMessageHandler->read()")
		self._read()

		if self._jsonheader_len is None:
			self.process_protoheader()

		if self._jsonheader_len is not None:
			if self.jsonheader is None:
				self.process_jsonheader()

		if self.jsonheader:
			if self.request is None:
				self.process_request()

	""" Write a message to the client till the full message has been sent """
	def write(self):
		print("TMessageHandler->write()")
		if self.request:
			if not self.response_created:
				self.create_response()
		self._write()

	def close(self):
		print("TMessageHandler->close()")
		try:
			self.selector.unregister(self.sock)
		except Exception as e:
			print(
				f"Error: selector.unregister() exception for "
				f"{self.addr}: {e!r}"
			)

		try:
			self.sock.close()
		except OSError as e:
			print(f"Error: socket.close() exception for {self.addr}: {e!r}")
		finally:
			# Delete reference to socket object for garbage collection
			self.sock = None

	def process_protoheader(self):
		print("TMessageHandler->process_protoheader()")
		hdrlen = 2
		if len(self._recv_buffer) >= hdrlen:
			self._jsonheader_len = struct.unpack(
				">H", self._recv_buffer[:hdrlen]
			)[0]
			self._recv_buffer = self._recv_buffer[hdrlen:]

	"""
	
	"""
	def process_jsonheader(self):
		print("TMessageHandler->process_jsonheader()")
		hdrlen = self._jsonheader_len
		if len(self._recv_buffer) >= hdrlen:
			self.jsonheader = self._json_decode(
				self._recv_buffer[:hdrlen], "utf-8"
			)
			self._recv_buffer = self._recv_buffer[hdrlen:]
			for reqhdr in (
				"byteorder",
				"content-length",
				"content-type",
				"content-encoding",
			):
				if reqhdr not in self.jsonheader:
					raise ValueError(f"Missing required header '{reqhdr}'.")

	def process_request(self) -> Optional[dict]:
		print("TMessageHandler->process_request()")
		content_len = self.jsonheader["content-length"]
		if not len(self._recv_buffer) >= content_len:
			return None
		self.request = {
			"cmd": "nop"
		}
		data = self._recv_buffer[:content_len]
		self._recv_buffer = self._recv_buffer[content_len:]
		if self.jsonheader["content-type"] == "text/json":
			encoding = self.jsonheader["content-encoding"]
			request: dict = self._json_decode(data, encoding)
			action = request.get("cmd")
			if action == "client":
				client_action = request.get(action)
				if client_action == "new": # Connect a new client to the server
					cid = f"CID#{self.addr}"

					self.request = {
						"cmd": action,
						action: client_action,
						"cid": cid,
						"x": request.get("x"),
						"y": request.get("y"),
					}
			elif action == "fos":
				x = request.get("x")
				y = request.get("y")
				z = request.get("z")
				m = request.get("m")
				r = request.get("r")
				view = self.world.field_of_sense(x=x, y=y, z=z, m=m, r=r)

				self.request = {
					"cmd": action,
					"x": x,
					"y": y,
					"z": z,
					"m": m,
					"r": r,
					"fos": view.tolist()
				}
		# Set selector to listen for write events, we're done reading.
		self._set_selector_events_mask("w")

	def create_response(self):
		print("TMessageHandler->create_response()")
		if self.jsonheader["content-type"] == "text/json":
			response = self._create_response_json_content()
		message = self._create_message(**response)
		self.response_created = True
		self._send_buffer += message
