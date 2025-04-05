from typing import Tuple
from entities import TActor

from worlds import TWorld

"""
TAction is the base class
"""
class TAction:
	def run(self, actor: TActor):
		self.actor = actor

	def run(self) -> None:
		raise NotImplementedError()

"""
TEscapeAction stops the actor playing the game
"""
class TEscapeAction(TAction):
	def run(self) -> None:
		self.actor.data["playing"] = False

"""
TMoveAction moves the actor in one direction
"""
class TMoveAction(TAction):
	def __init__(self, actor: TActor, dx: int, dy: int):
		super().__init__(actor)
		self.dx = dx
		self.dy = dy

	@property
	def dest_xy(self) -> Tuple[int, int]:
		return self.actor.data['x'] + self.dx, self.actor.data['y'] + self.dy

	def run(self):
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
					self.actor.data["x"] = gateway["x"]
					self.actor.data["y"] = gateway["y"]
					self.actor.data["m"] = gateway["m"]
				else:
					# Move to x, y coordinate
					self.actor.data["x"] = dest_x
					self.actor.data["y"] = dest_y