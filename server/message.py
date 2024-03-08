import sys
import selectors, socket
import json
import io
import struct

class TMessage:
	def __init__(self, selector: selectors.BaseSelector, sock: socket.socket, addr):
		self.selector: selectors.BaseSelector = selector
		self.sock: socket.socket = sock
		self.addr = addr
		self._recv_buffer = b""
		self._send_buffer = b""
		self._jsonheader_len = None
		self.jsonheader = None
		self.request = None
		self.response_created = False

	""" Switch message handling between read and write """
	def _set_selector_events_mask(self, mode):
		if mode == "r":
			events = selectors.EVENT_READ
		elif mode == "w":
			events = selectors.EVENT_WRITE
		elif mode == "rw":
			events = selectors.EVENT_READ | selectors.EVENT_WRITE
		else:
			raise ValueError(f"Invalid events mask mode {mode!r}.")
		self.selector.modify(self.sock, events, data=self)

	""" 1. Read client data """
	def _read(self):
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
		if self._send_buffer:
			print(f"Sending {self._send_buffer!r} to {self.addr}")
			try:
				# Should be ready to write
				sent = self.sock.send(self._send_buffer)
			except BlockingIOError:
				# Resource temporarily unavailable (errno EWOULDBLOCK)
				pass
			else:
				self._send_buffer = self._send_buffer[sent:]
				# Close when the buffer is drained. The response has been sent.
				if sent and not self._send_buffer:
					self.close()

	def _json_encode(self, obj, encoding):
		return json.dumps(obj, ensure_ascii=False).encode(encoding)

	def _json_decode(self, json_bytes, encoding):
		tiow = io.TextIOWrapper(
			io.BytesIO(json_bytes), encoding=encoding, newline=""
		)
		obj = json.load(tiow)
		tiow.close()
		return obj

	def _create_message(
		self, *, content_bytes, content_type, content_encoding
	):
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

	""" 1.1 Prepare the content as json """
	def _create_response_json_content(self):
		action = self.request.get("cmd")
		if action == "fos":
			x = self.request.get("x") # Get coordinates (x, y, z)
			y = self.request.get("y")
			z = self.request.get("z")
			r = self.request.get("r") # Get radius of FOS
			i = self.request.get("i") # Get client ID
			#
			# world.get_fos(x, y, z, r) - get the fov and all the actors and items in the fov
			# fos structure = {"l": int, "a": array of actor objects {"c": char, "i": uuid}}
			fos = self.world.fov(x, y, z, r)
			content = {
				"res": "ok",
				"fos": fos
			}
		else:
			content = {"res": "error", "msg": f"Invalid action '{action}'."}
		content_encoding = "utf-8"
		response = {
			"content_bytes": self._json_encode(content, content_encoding),
			"content_type": "text/json",
			"content_encoding": content_encoding,
		}
		return response

	def _create_response_binary_content(self):
		response = {
			"content_bytes": b"First 10 bytes of request: "
			+ self.request[:10],
			"content_type": "binary/custom-server-binary-type",
			"content_encoding": "binary",
		}
		return response

	def process_events(self, mask):
		if mask & selectors.EVENT_READ:
			self.read()
		if mask & selectors.EVENT_WRITE:
			self.write()

	def read(self):
		# 1. Read client data
		self._read()

		# 2. Process the proto header of the client message
		if self._jsonheader_len is None:
			self.process_protoheader()

		# 3. Process the json header of the client message
		if self._jsonheader_len is not None:
			if self.jsonheader is None:
				self.process_jsonheader()

		# 4. Process the request of the client message
		if self.jsonheader:
			if self.request is None:
				self.process_request()

	def write(self):
		# 1. Create a message to send to the client
		if self.request:
			if not self.response_created:
				self.create_response()

		# 2. Write data to the client
		self._write()

	def close(self):
		print(f"Closing connection to {self.addr}")
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

	""" 2. Process the proto header of the client message """
	# Extract the first 2 bytes to get the length of the json header
	def process_protoheader(self):
		hdrlen = 2
		if len(self._recv_buffer) >= hdrlen:
			self._jsonheader_len = struct.unpack(
				">H", self._recv_buffer[:hdrlen]
			)[0]
			self._recv_buffer = self._recv_buffer[hdrlen:]

	""" 3. Process the json header of the client message """
	# Extract the json header when the length of data has been received
	def process_jsonheader(self):
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

	""" 4. Process the request of the client message """
	def process_request(self):
		content_len = self.jsonheader["content-length"]
		if not len(self._recv_buffer) >= content_len:
			return
		# Request has been received, process and react
		data = self._recv_buffer[:content_len]
		self._recv_buffer = self._recv_buffer[content_len:]
		if self.jsonheader["content-type"] == "text/json":
			encoding = self.jsonheader["content-encoding"]
			self.request = self._json_decode(data, encoding)
			print(f"Received request {self.request!r} from {self.addr}")
		else:
			# Binary or unknown content-type
			self.request = data
			print(
				f"Received {self.jsonheader['content-type']} "
				f"request from {self.addr}"
			)
		# Set selector to listen for write events, we're done reading.
		self._set_selector_events_mask("w")

	""" 1. Create a message to send to the client """
	def create_response(self):
		if self.jsonheader["content-type"] == "text/json":
			# 1.1 Prepare the content as json
			response = self._create_response_json_content()
		else:
			# Binary or unknown content-type
			response = self._create_response_binary_content()
		# 1.2 Create the message itself
		message = self._create_message(**response)
		self.response_created = True
		# 1.3 Append the send buffer with the message
		self._send_buffer += message
