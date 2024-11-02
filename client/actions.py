import socket
import pickle

import config

from entities import TEntity
from game_map import TGameMap

class TAction:
	def run(self, entity: TEntity, game_map: TGameMap):
		pass

class TEscapeAction(TAction):
	def run(self, entity: TEntity, game_map: TGameMap):
		command = {
			"c": "disconnect",
			"i": entity.cuid,
		}
		entity.data["game_active"] = False

class TMoveAction(TAction):
	def __init__(self, dx: int, dy: int):
		super().__init__()
		self.dx = dx
		self.dy = dy

	def run(self, entity: TEntity, game_map: TGameMap):
		# Inform server of action and get result
		command = {
			"c": "mov",
			"i": entity.cuid,
			"x": entity.data["x"],
			"y": entity.data["y"],
		}
		entity.client.sendall(bytes(pickle.dumps(command)))
		data = entity.client.recv(1024)

		print(f"Server sent {pickle.loads(data)}")
		if game_map.tiles["walkable"][entity.data["x"] + self.dx, entity.data["y"] + self.dy]:
			entity.data["x"] += self.dx
			entity.data["y"] += self.dy
