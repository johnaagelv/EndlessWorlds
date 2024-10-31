import pickle
import socket
import config
import uuid

from typing import Tuple

from actions import TAction

class TEntity:
	"""
	A generic object to represent players, enemies, items, etc.
	"""
	def __init__(
		self,
		x: int,
		y: int,
		face: str,
		colour: Tuple[int, int, int],
	):
		self.data = {
			"x": x,
			"y": y,
			"face": face,
			"colour": colour,
			"game_active": True,
		}
		self._connect()
		self._identify()
		print(f"Connected as {self.cuid}")

	"""
	Identify the client to the server
	"""
	def _identify(self, cuid: str = None):
		command = {
			"c": "connect",
		}
		if cuid is not None:
			command["i"] = cuid

		self.client.sendall(bytes(pickle.dumps(command)))
		data = self.client.recv(1024)
		result = pickle.loads(data)
		self.cuid = result["i"] # Client unique ID from the server

	"""
	Establish a connection to the server
	"""
	def _connect(self):

		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect((config.servers[0]["host"], config.servers[0]["port"]))

	def run(self, action: TAction):
		action.run(self)
