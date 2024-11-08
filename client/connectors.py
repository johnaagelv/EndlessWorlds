from typing import Any, Dict
import types
import selectors
import socket
import pickle

class TConnector:
	"""
	Initialize the connection to a HUB server
	"""
	def __init__(self, host: str, port: int):
		self.host = host
		self.port = port
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect((self.host, self.port))
		self.client.setblocking(False)
		self.sel = selectors.DefaultSelector()
		self.sel.register(self.client, selectors.EVENT_READ | selectors.EVENT_WRITE, data=None)

	def execute(self, command: Dict) -> Dict:
		self.client.sendall(bytes(pickle.dumps(command)))
		data = self.client.recv(1024)
		print(f"{data!r}")
		return pickle.loads(data)
