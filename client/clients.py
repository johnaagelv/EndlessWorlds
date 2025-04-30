from typing import Any
import logging
logger = logging.getLogger("EWClient")

import sys
import selectors
import socket
import traceback
import json
import io
import struct
import pickle

import numpy as np

from entities import TActor
from worlds import TWorld

class TClient:
	def __init__(self):
		logger.debug(f"TClient->__init__()")
		self.sel = selectors.DefaultSelector()

	""" Start connection to the specified server with the provided request """
	def start_connection(self, host, port, request):
		logger.debug(f"TClient->start_connection( host, port, request )")
		addr = (host, port)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setblocking(False)
		sock.connect_ex(addr)
		events = selectors.EVENT_READ | selectors.EVENT_WRITE
		message = TMessage(self.sel, sock, addr, request)
		self.sel.register(sock, events, data=message)

	def run(self, player: TActor) -> Any:
		logger.debug(f"TClient->run( actor )")
		events = self.sel.select(timeout=5.0)
		for key, mask in events:
			message: TMessage = key.data
			try:
				message.process_events(mask)
				if message.sock is None:

					if message.response['cmd'] == 'new':
						logger.info(f"TClient initializing new world")
						player.data['x'] = message.response['entry_point'][0]
						player.data['y'] = message.response['entry_point'][1]
						player.data['z'] = message.response['entry_point'][2]
						player.data['m'] = message.response['entry_point'][3]
						player.data['world'] = TWorld(player, message.response['map_sizes'])
					elif message.response['cmd'] == 'fos':
						logger.info(f"TClient applying FOS data")
						fos = message.response['fos']
						x_min = fos.get("x_min")
						x_max = fos.get("x_max")
						y_min = fos.get("y_min")
						y_max = fos.get("y_max")
						view = fos.get("view")
						gateways = fos.get("gateways")
						temp = np.array(view)
						player.data["world"].maps[player.data["m"]]["tiles"][x_min:x_max, y_min:y_max] = temp
						player.data["world"].maps[player.data["m"]]["gateways"] = gateways

			except Exception:
				logger.warning(
					f"TClient: Error: Exception for {message.addr}:\n"
					f"{traceback.format_exc()}"
				)
				message.close()
		if not self.sel.get_map():
			return False
		return True
		
class TMessage:
	def __init__(self, selector, sock, addr, request):
		logger.debug(f"TMessage->__init__( selector, sock, addr, request )")
		self.selector = selector
		self.sock = sock
		self.addr = addr
		self.request = request
		self._recv_buffer = b""
		self._send_buffer = b""
		self._request_queued = False
		self._jsonheader_len = None
		self.jsonheader = None
		self.response = None

	def _set_selector_events_mask(self, mode):
		logger.debug(f"TMessage->_set_selector_events_mask( mode )")
		"""Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
		if mode == "r":
			events = selectors.EVENT_READ
		elif mode == "w":
			events = selectors.EVENT_WRITE
		elif mode == "rw":
			events = selectors.EVENT_READ | selectors.EVENT_WRITE
		else:
			raise ValueError(f"Invalid events mask mode {mode!r}.")
		self.selector.modify(self.sock, events, data=self)

	def _read(self):
		logger.debug(f"TMessage->_read()")
		try:
			# Should be ready to read
			data = self.sock.recv(4096)
		except BlockingIOError:
			# Resource temporarily unavailable (errno EWOULDBLOCK)
			pass
		else:
			if data:
				self._recv_buffer += data
			else:
				raise RuntimeError("Peer closed.")

	def _write(self):
		logger.debug(f"TMessage->_write()")
		if self._send_buffer:
#			print(f"Sending {self._send_buffer!r} to {self.addr}")
			try:
				# Should be ready to write
				sent = self.sock.send(self._send_buffer)
			except BlockingIOError:
				# Resource temporarily unavailable (errno EWOULDBLOCK)
				pass
			else:
				self._send_buffer = self._send_buffer[sent:]

	def _json_encode(self, obj, encoding):
		logger.debug(f"TMessage->_json_encode( obj, encoding )")
		return json.dumps(obj, ensure_ascii=False).encode(encoding)

	def _json_decode(self, json_bytes, encoding):
		logger.debug(f"TMessage->_json_decode( json_bytes, encoding )")
		tiow = io.TextIOWrapper(
			io.BytesIO(json_bytes), encoding=encoding, newline=""
		)
		obj = json.load(tiow)
		tiow.close()
		return obj

	def _create_message(
		self, *, content_bytes, content_type, content_encoding
	):
		logger.debug(f"TMessage->_create_message( content_bytes, content_type, content_encoding )")
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

	def _process_response_json_content(self):
		logger.debug(f"TMessage->_process_response_json_content()")
		content = self.response
		result = content.get("result")

	def _process_response_binary_content(self):
		logger.debug(f"TMessage->_process_response_binary_content()")
		content = self.response

	def process_events(self, mask):
		logger.debug(f"TMessage->process_events( mask )")
		if mask & selectors.EVENT_READ:
			self.read()
		if mask & selectors.EVENT_WRITE:
			self.write()

	def read(self):
		logger.debug(f"TMessage->read()")
		self._read()

		if self._jsonheader_len is None:
			self.process_protoheader()

		if self._jsonheader_len is not None:
			if self.jsonheader is None:
				self.process_jsonheader()

		if self.jsonheader:
			if self.response is None:
				self.process_response()

	def write(self):
		logger.debug(f"TMessage->write()")
		if not self._request_queued:
			self.queue_request()

		self._write()

		if self._request_queued:
			if not self._send_buffer:
				# Set selector to listen for read events, we're done writing.
				self._set_selector_events_mask("r")

	def close(self):
		logger.debug(f"TMessage->close()")
		try:
			self.selector.unregister(self.sock)
		except Exception as e:
			logger.debug(
				f"Error: selector.unregister() exception for "
				f"{self.addr}: {e!r}"
			)

		try:
			self.sock.close()
		except OSError as e:
			logger.debug(f"Error: socket.close() exception for {self.addr}: {e!r}")
		finally:
			# Delete reference to socket object for garbage collection
			self.sock = None

	def queue_request(self):
		logger.debug(f"TMessage->queue_request()")
		content = self.request
		content_type = "binary/custom-server-binary-type"
		content_encoding = "binary"
		if content_type == "text/json":
			req = {
				"content_bytes": self._json_encode(content, content_encoding),
				"content_type": content_type,
				"content_encoding": content_encoding,
			}
		else:
			req = {
				"content_bytes": pickle.dumps(content),
				"content_type": content_type,
				"content_encoding": content_encoding,
			}
		message = self._create_message(**req)
		self._send_buffer += message
		self._request_queued = True

	def process_protoheader(self):
		logger.debug(f"TMessage->process_protoheader()")
		hdrlen = 2
		if len(self._recv_buffer) >= hdrlen:
			self._jsonheader_len = struct.unpack(
				">H", self._recv_buffer[:hdrlen]
			)[0]
			self._recv_buffer = self._recv_buffer[hdrlen:]

	def process_jsonheader(self):
		logger.debug(f"TMessage->process_jsonheader()")
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
					logger.error(f"Missing required header '{reqhdr}'.")

	def process_response(self):
		logger.debug(f"TMessage->process_response()")
		content_len = self.jsonheader["content-length"]
		if len(self._recv_buffer) < content_len:
			return
		data = self._recv_buffer[:content_len]
		self._recv_buffer = self._recv_buffer[content_len:]
		if self.jsonheader["content-type"] == "text/json":
			encoding = self.jsonheader["content-encoding"]
			self.response = self._json_decode(data, encoding)
			self._process_response_json_content()
		else:
			# Binary or unknown content-type
			self.response = pickle.loads(data)
			logger.debug(
				f"- Received {self.jsonheader['content-type']} "
				f"response from {self.addr}"
			)
			logger.debug(f"- content {self.response!r}")
			# self._process_response_binary_content()
		# Close when response has been processed
		self.close()
