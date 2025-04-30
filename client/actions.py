from typing import Tuple
import logging
logger = logging.getLogger("EWClient")

from entities import TActor

from worlds import TWorld

"""
TAction is the base class
"""
class TAction:
	def __init__(self, actor: TActor):
		logger.debug(f"TAction->__init__( actor )")
		self.actor = actor

	def run(self) -> None:
		logger.debug(f"TAction->run()")
		raise NotImplementedError()

"""
TEscapeAction stops the actor playing the game
"""
class TEscapeAction(TAction):
	def run(self) -> None:
		logger.debug(f"TEscapeAction->run()")
		self.actor.data["playing"] = False

"""
TMoveAction moves the actor in one direction
"""
class TMoveAction(TAction):
	def __init__(self, actor: TActor, dx: int, dy: int):
		logger.debug(f"TMoveAction->__init__( actor, dx, dy )")
		super().__init__(actor)
		self.dx = dx
		self.dy = dy

	@property
	def dest_xy(self) -> Tuple[int, int]:
		logger.debug(f"TMoveAction->dest_xy")
		return self.actor.data['x'] + self.dx, self.actor.data['y'] + self.dy

	def run(self):
		logger.debug(f"TMoveAction->run()")
		world: TWorld = self.actor.data["world"]
		map = world.maps[self.actor.data["m"]]
		dest_x, dest_y = self.dest_xy

		# Check in bounds of the map
		if world.in_bounds(dest_x, dest_y, self.actor.data['m']):
			# Check if walkable
			if map["tiles"]["walkable"][dest_x, dest_y]:
				if world.in_gateway(dest_x, dest_y, self.actor.data["m"]):
					gateway = world.go_gateway(dest_x, dest_y, self.actor.data["m"])
					# Move to x, y coordinate in map number m
					self.actor.data["x"] = gateway["gateway"]["x"]
					self.actor.data["y"] = gateway["gateway"]["y"]
					self.actor.data["m"] = gateway["gateway"]["m"]
				else:
					# Move to x, y coordinate
					self.actor.data["x"] = dest_x
					self.actor.data["y"] = dest_y

class TStairAction(TAction):
	@property
	def current_xy(self) -> Tuple[int, int]:
		logger.debug(f"TStairAction->current_xy")
		return self.actor.data['x'], self.actor.data['y']

	def run(self):
		logger.debug(f"TStairAction->run()")
		world: TWorld = self.actor.data["world"]
		map = world.maps[self.actor.data["m"]]
		dest_x, dest_y = self.current_xy
		if world.in_bounds(dest_x, dest_y, self.actor.data['m']):
			# Check if walkable
			if map["tiles"]["walkable"][dest_x, dest_y]:
				gateway = world.go_gateway(dest_x, dest_y, self.actor.data["m"])
				if gateway is not None:
					# Move to x, y coordinate in map number m
					self.actor.data["x"] = gateway['gateway']["x"]
					self.actor.data["y"] = gateway['gateway']["y"]
					self.actor.data["m"] = gateway['gateway']["m"]
