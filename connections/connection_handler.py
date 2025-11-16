from __future__ import annotations

import selectors
import json
import io
import struct
import socket
import pickle
import logging

logger = logging.getLogger("EWlogger")

"""
TConnectionHandler handles communication between client and server
"""
class TConnectionHandler:
	_jsonheader_len: int = -1
	jsonheader: dict = {}
	_mode_switch_matrix: dict = {
		"r": selectors.EVENT_READ,
		"w": selectors.EVENT_WRITE,
		"rw": selectors.EVENT_READ | selectors.EVENT_READ
	}

	"""
	Initialize the communicator
	"""
	def __init__(self, primary_selector: selectors.BaseSelector, client_socket: socket.socket, addr: str):
		logger.debug(f"{__class__.__name__}->__init__( selector, sock, addr )")
		self.primary_selector = primary_selector
		self.client_socket = client_socket
		self.addr = addr # Client address as IP:PORT string
		self.message: dict = {} # Message received or to be sent
		self._buffer: bytes = b"" # Buffer for received and sent bytes
		self.protoheader_state = False
		self.jsonheader_state = False
		self.content_state = False
	
	# Switch primary selector mode to ´r', 'w', or ´rw'
	def _set_selector_events_mask(self, mode: str):
		logger.debug(f"{__class__.__name__}->_set_selector_events_mask( {mode} )")
		# Set selector to listen for events: mode is 'r', 'w', or 'rw'
		event_mode = self._mode_switch_matrix[mode]
		self.primary_selector.modify(self.client_socket, event_mode, data=self)

	# Send a message	
	def prepare_to_send(self):
		logger.debug(f"{__class__.__name__}->prepare_response( request )")
		self._set_selector_events_mask("w")

	"""
	Dispatch the message
	"""
	def dispatch(self, mask: int) -> bool:
		logger.debug(f"{__class__.__name__}->dispatch( {mask} )")
		if mask == selectors.EVENT_READ:
			return self.receive()
		else:
			return self.transmit()

	"""
	Close down the communication
	"""
	def close(self):
		logger.debug(f"{__class__.__name__}->close()")
		try:
			self.primary_selector.unregister(self.client_socket)
		except Exception as e:
			logger.warning(
				f"Error: selector.unregister() exception for "
				f"{self.addr}: {str(e)}"
			)
		try:
			self.client_socket.close()
		except OSError as e:
			logger.warning(f"Error: socket.close() exception for {self.addr}: {str(e)}")
		finally:
			# Delete reference to socket object for garbage collection
			del(self.client_socket)

	"""
	Read bytes from the connection into the buffer
	"""
	def _read(self):
		logger.debug(f"{__class__.__name__}->_read()")
		try:
			data = self.client_socket.recv(65536)
		except BlockingIOError:
			# Ignore that resource temporarily unavailable (errno EWOULDBLOCK)
			pass
		else:
			if data:
				self._buffer += data
			else:
				logger.warning(f"{__class__.__name__} peer closed.")
				self.close()

	"""
	Transform JSON into data using the specified encoding
	"""
	def _json_decode(self, json_bytes: bytes, encoding: str):
		logger.debug(f"{__class__.__name__}->_json_decode( json_bytes, encoding {encoding} )")
		logger.debug(f"- {json_bytes}")
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
		header_keys = self.jsonheader.keys()
		if "content-length" in header_keys:
			content_len = self.jsonheader["content-length"]
			if len(self._buffer) >= content_len:
				# Content received, process
				logger.debug(f"- content ready {content_len}")
				self.content_state = True
				data = self._buffer[:content_len]
				self._buffer = self._buffer[content_len:]
				if self.jsonheader["content-type"] == "text/json":
					encoding = self.jsonheader["content-encoding"]
					self.message = self._json_decode(data, encoding)
#					logger.debug(f"- request is {self.message}")
				else:
					# Extract the request from the content
					self.message = pickle.loads(data)
					logger.debug(f"- request is {self.message}")
				return True
		return False # Content not received in full yet, stop processing

	"""
	Process the json header when fully received
	"""
	def process_jsonheader(self):
		logger.debug(f"{__class__.__name__}->process_jsonheader()")
		hdrlen = self._jsonheader_len
		if len(self._buffer) >= hdrlen:
			# Header received, process
			logger.debug("- jsonheader ready")
			self.jsonheader_state = True
			self.jsonheader = self._json_decode(self._buffer[:hdrlen], "utf-8")
			self._buffer = self._buffer[hdrlen:]
			# Check that required headers are received
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
		if len(self._buffer) >= hdrlen:
			logger.debug("- protoheader ready")
			self.protoheader_state = True
			self._jsonheader_len = struct.unpack(">H", self._buffer[:hdrlen])[0]
			self._buffer = self._buffer[hdrlen:]

	"""
	Receive the message from the sender
	- read the message in parts till the full message has been received
	"""
	def receive(self) -> bool:
		logger.debug(f"{__class__.__name__}->receive()")
		self._read()
		if not self.protoheader_state:
			self.process_protoheader()
		if self.protoheader_state:
			if not self.jsonheader_state:
				self.process_jsonheader()
		if self.jsonheader_state:
			if not self.content_state:
				return self.process_request()
		return False

	"""
	Transmit the message to the recipient
	"""
	def transmit(self) -> bool:
		logger.debug(f"{__class__.__name__}->transmit()")
		return self._write()

	"""
	Write bytes to the connection from the buffer
	"""
	def _write(self) -> bool:
		blen = len(self._buffer)
		logger.debug(f"{__class__.__name__}->_write( {blen} bytes)")
		if self._buffer:
			try:
				sent = self.client_socket.send(self._buffer)
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
	Fill the buffer
	"""
	def buffer(self, data: bytes):
		self._buffer = data

