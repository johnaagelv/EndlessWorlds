import socket
import selectors
import uuid
import pickle
import traceback

from procgen import generate_dungeon
from messages import TServerMessage

class TServer:
	def __init__(self, host: str="127.0.0.1", port: int=65432):
		self.host = host
		self.port = port
		self.sel = selectors.DefaultSelector()
		self.game_map = generate_dungeon(80, 45)
		self.clients = dict()

	def accept_wrapper(self, client_socket: socket):
		client_connection, addr = client_socket.accept()
		client_connection.setblocking(False)
		message = TServerMessage(self.sel, client_connection, addr)
		events = selectors.EVENT_READ | selectors.EVENT_WRITE
		self.sel.register(client_connection, events, data=message)

	def run(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_connection:
			server_connection.bind((self.host, self.port))
			server_connection.listen()
			server_connection.setblocking(False)
			self.sel.register(server_connection, selectors.EVENT_READ, data=None)
			try:
				while True:
					events = self.sel.select(timeout = None)

					for key, mask in events:
						if key.data is None:
							self.accept_wrapper(key.fileobj)
						else:
							message: TServerMessage = key.data
							try:
								message.process_events(mask)
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