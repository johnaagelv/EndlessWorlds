from typing import Any, Dict
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

	def execute(self, command: Dict) -> Dict:
		print(f"Sending {command!r}")
		self.client.sendall(bytes(pickle.dumps(command)))
		data = self.client.recv(1024)
		print(f"Received {data!r}")
		return pickle.loads(data)
