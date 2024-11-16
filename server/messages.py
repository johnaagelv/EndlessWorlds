import struct
import selectors
import socket
import json
import io
import sys

from tcod.map import compute_fov

MSG_ENCODING = "utf-8"

class TMessage:
	def __init__(self, selector: selectors.BaseSelector, sock: socket.socket, addr, game_map):
		self.selector = selector # Selector from the Server
		self.sock = sock
		self.addr = addr
		self.game_map = game_map
		self._recv_buffer = b""
		self._send_buffer = b""
		self._jsonheader_len = None
		self.jsonheader = None
		self.request = None
		self._request_queued = False
		self.response = None
		self.response_created = False

	""" Switch to the specified mode """
	def _set_selector_events_mask(self, mode):
		print("TMessage->_set_selector_events_mask(mode)")
		if mode == "r":
			events = selectors.EVENT_READ
		elif mode == "w":
			events = selectors.EVENT_WRITE
		elif mode == "rw":
			events = selectors.EVENT_READ | selectors.EVENT_WRITE
		else:
			raise ValueError(f"Invalid events mask mode {mode!r}.")
		self.selector.modify(self.sock, events, data=self)

	
	"""
	Read bytes from the connection into the receive buffer
	"""
	def _read(self):
		print("TMessage->_read()")
		try:
			data = self.sock.recv(1024)
		except BlockingIOError:
			pass
		else:
			if data:
				self._recv_buffer += data
			else:
				self.close()

	"""
	Write bytes to the connection from the send buffer
	"""
	def _write(self):
		print("TMessage->_write()")
		if self._send_buffer:
			try:
				sent = self.sock.send(self._send_buffer)
			except BlockingIOError:
				pass
			else:
				self._send_buffer = self._send_buffer[sent:]
				if sent and not self._send_buffer:
					self.close()

	"""
	Encode data into json format
	"""
	def _json_encode(self, obj, encoding):
		print("TMessage->_json_encode(obj, encoding)")
		return json.dumps(obj, ensure_ascii=False).encode(encoding)

	"""
	Decode data from json format
	"""
	def _json_decode(self, json_bytes, encoding):
		print("TMessage->_json_decode(json_bytes, encoding)")
		tiow = io.TextIOWrapper(
			io.BytesIO(json_bytes), encoding=encoding, newline=""
		)
		obj = json.load(tiow)
		tiow.close()
		return obj
	
	"""
	Create a complete message
	"""
	def _create_message(self, content_bytes):
		print("TMessage->_create_message(content_bytes)")
		jsonheader = {
			"content-length": len(content_bytes),
		}
		jsonheader_bytes = self._json_encode(jsonheader, MSG_ENCODING)
		message_hdr = struct.pack(">H", len(jsonheader_bytes))
		message = message_hdr + jsonheader_bytes + content_bytes
		return message

	"""
	Encode the content
	"""
	def _create_response_json_content(self):
		print("TMessage->_create_response_json_content()")
		response = {"content_bytes": self._json_encode(self.request, MSG_ENCODING)}
		return response

	"""
	Process events from the selector
	"""	
	def process_events(self, mask):
		print("TMessage->process_events()")
		if mask & selectors.EVENT_READ:
			self.read()
		if mask & selectors.EVENT_WRITE:
			self.write()

	"""
	Retrieve a complete message - protoheader, jsonheader, content
	"""
	def read(self) -> bool:
		print("TMessage->read()")
		message_state = False
		self._read()
		# Try to get the protoheader (2 bytes)
		if self._jsonheader_len is None:
			self.process_protoheader()
		# Try to get the jsonheader (content-length + value)
		if self._jsonheader_len is not None:
			if self.jsonheader is None:
				self.process_jsonheader()
		# Try to get the content (get the command)
		if self.jsonheader:
			if self.request is None:
				message_state = self.process_request()
		return message_state

	"""
	Deliver a complete message - protoheader, jsonheader, content
	"""	
	def write(self):
		print("TMessage->write()")
		# Prepare a message when content is available
		if self.request:
			if not self.response_created:
				self.create_response()
		# Try to send the message
		self._write()

	def close(self):
		print("TMessage->close()")
		try:
			self.selector.unregister(self.sock)
		except Exception as e:
			print(
				f"Error: selector.unregister() exception for"
		 		f"{self.addr}: {e!r}"
			)
		try:
			self.sock.close()
		except OSError as e:
			print(f"Error: socket.close() exception for {self.addr}: {e!r}")
		finally:
			self.sock = None

	"""
	Retrieve the protoheader from the receive buffer
	"""
	def process_protoheader(self):
		print("TMessage->process_protoheader()")
		hdrlen = 2
		if len(self._recv_buffer) >= hdrlen:
			self._jsonheader_len = struct.unpack(">H", self._recv_buffer[:hdrlen])[0]
			self._recv_buffer = self._recv_buffer[hdrlen:]
	
	"""
	Retrieve the jsonheader from the receive buffer
	"""
	def process_jsonheader(self):
		print("TMessage->process_jsonheader()")
		hdrlen = self._jsonheader_len
		if len(self._recv_buffer) >= hdrlen:
			self.jsonheader = self._json_decode(
				self._recv_buffer[:hdrlen], MSG_ENCODING
			)
			self._recv_buffer = self._recv_buffer[hdrlen:]
			print(f"- jsonheader: {self.jsonheader!r}")
			# Validate that json header is complete!
#			for reqhdr in ("content-length"):
			reqhdr = "content-length"
			if reqhdr not in self.jsonheader:
				raise ValueError(f"Message missing required header '{reqhdr}'")

	"""
	Retrieve the content from the receive buffer
	"""
	def process_request(self) -> bool:
		print(f"TMessage->process_request()")
		content_len = self.jsonheader["content-length"]
		# Is all content received?
		if not len(self._recv_buffer) >= content_len:
			return False
		data = self._recv_buffer[:content_len]
		self._recv_buffer = self._recv_buffer[content_len:]
		encoding = MSG_ENCODING
		request = self._json_decode(data, encoding)
		print(f"- request: {request!r}")
		# PROCESS THE REQUEST FROM THE CLIENT
		# update client position (x, y, z)
		x, y, z = request["x"], request["y"], request["z"]
		fov = compute_fov(
			self.game_map.tiles["transparent"],
			(x, y),
			radius=4
		)
		#self.request = {"fov":fov.tolist(), "x": x, "y": y, "radius": 8}
		self.request = {
			"cmd": "fov",
			"x": x,
			"y": y,
			"z": z,
			"r": 4,
			"fov": fov.tolist(),
		}
		# get FOS for the client (field of sense), usually that is FOV (field of view)
		# get FOA for the client (field of actors), actors within the FOS
		# package the information and send it back to the client
		# Set selector to listen for write events, we're done reading.
		self._set_selector_events_mask("w")

	def create_response(self):
		print(f"TMessage->create_response()")
		response = self._create_response_json_content()
		message = self._create_message(**response)
		self.response_created = True
		self._send_buffer += message