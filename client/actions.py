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
		}
		entity.data["playing"] = False
		

class TMoveAction(TAction):
	def __init__(self, dx: int, dy: int):
		super().__init__()
		self.dx = dx
		self.dy = dy

	def run(self, entity: TEntity, game_map: TGameMap):
		# Inform server of action and get result
		command = {
			"c": "mov",
			"x": entity.data["location"]["x"],
			"y": entity.data["location"]["y"],
			"z": entity.data["location"]["z"],
			"r": 4,
		}
		data = entity.client.execute(command)

		if game_map.tiles["walkable"][entity.data["location"]["x"] + self.dx, entity.data["location"]["y"] + self.dy]:
			entity.data["location"]["x"] += self.dx
			entity.data["location"]["y"] += self.dy
