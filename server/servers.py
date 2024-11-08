import socket
import selectors
import uuid
import pickle
import traceback

from procgen import generate_dungeon
from messages import TMessage

class TServer:
	def __init__(self, host: str="127.0.0.1", port: int=65432):
		self.host = host
		self.port = port
		self.sel = selectors.DefaultSelector()
		self.game_map = generate_dungeon(80, 45)
		self.clients = dict()
		
	def service_connection(self, key, mask):
		sock = key.fileobj
		data = key.data
		if mask & selectors.EVENT_READ:
			recv_data = sock.recv(1024)
			if recv_data:
				command = pickle.loads(recv_data)
				result = command
				if "c" in command.keys():
					if command["c"] == "connect":
						# Establish client connection
						if "i" in command.keys():
							if command["i"] in self.clients.keys():
								pass
							else:
								self.clients[command["i"]] = command["i"]
						else:
							client = uuid.uuid1()
							self.clients[client] = client
							result["i"] = client
							# return the map size
							result["w"] = 80
							result["h"] = 45

					elif command["c"] == "mov":
						# Get the FOV at the x and y coordinate
						# Return the FOV
						result["c"] = "fov"
						x1 = command["x"] - command["r"]
						x2 = command["x"] + command["r"] + 1
						y1 = command["x"] - command["r"]
						y2 = command["x"] + command["r"] + 1
						result["a"] = self.game_map.tiles[x1:x2, y1:y2]

					else:
						result["c"] = "nop"
				else:
					result["c"] = "nop"

				data.outb = pickle.dumps(result)
			else:
				self.sel.unregister(sock)
				sock.close()
		if mask & selectors.EVENT_WRITE:
			if data.outb:
				sent = sock.send(data.outb)
				data.outb = data.outb[sent:]

	def accept_wrapper(self, client_socket: socket):
		client_connection, addr = client_socket.accept()
		client_connection.setblocking(False)
		message = TMessage(self.sel, client_connection, addr)
		events = selectors.EVENT_READ | selectors.EVENT_WRITE
		self.sel.register(client_connection, events, data=message)

	def run(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
			server.bind((self.host, self.port))
			server.listen()
			server.setblocking(False)
			self.sel.register(server, selectors.EVENT_READ, data=None)
			try:
				while True:
					events = self.sel.select(timeout = None)

					for key, mask in events:
						if key.data is None:
							self.accept_wrapper(key.fileobj)
						else:
							message: TMessage = key.data
							try:
								message_state = message.process_events(mask)
								if message_state:
									# Command has been received
									print(f"Command: {message.request!r}")
							except Exception:
								print(
									f"Main: Error: Exception for {message.addr}:\n"
									f"{traceback.format_exc()}"
								)
								message.close()
			except KeyboardInterrupt:
				pass
			finally:
				self.sel.close()