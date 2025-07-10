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
	
	def use(self, state: str = "energy", value: int = 0):
		self.actor.data['states'][state][0] -= value

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
	def __init__(self, actor: TActor, dx: int, dy: int, user_action: int = 0):
		logger.debug(f"TMoveAction->__init__( actor, dx, dy, user_action )")
		super().__init__(actor)
		self.dx = dx
		self.dy = dy
		self.direction = user_action

	"""
	Provides the move factor aka move speed
	"""
	@property
	def move_factor(self) -> int:
		logger.debug(f"TMoveAction->move_factor")
		try:
			move_factor = self.actor.data['actions']['move'][0]
		except:
			move_factor = 1 # Default move factor is always 1
		return move_factor
	
	"""
	Provides the coordinates of the destination
	"""
	@property
	def dest_xy(self) -> Tuple[int, int]:
		logger.debug(f"TMoveAction->dest_xy")
		x, y = self.actor.current_xy
		return x + self.dx, y + self.dy

	"""
	Execute the action
	"""
	def run(self):
		logger.info(f"TMoveAction->run()")
		world: TWorld = self.actor.world
		map_idx = self.actor.map_idx
		map = self.actor.map
		dest_x, dest_y = self.dest_xy
		# Check in bounds of the map
		if world.in_bounds(dest_x, dest_y, map_idx):
			# Check if walkable
			if map is not None:
				if map["tiles"]["walkable"][dest_x, dest_y]:
					self.use('energy', 1)
					if world.in_gateway(dest_x, dest_y, map_idx) or self.direction is not None:
						# Get the gateway information 
						gateway = world.go_gateway(dest_x, dest_y, map_idx, self.direction)
						# Move to x, y coordinate in map number m
						self.actor.data["x"] = gateway["gateway"]["x"]
						self.actor.data["y"] = gateway["gateway"]["y"]
						if gateway['gateway']['h'] == "":
							if map_idx != gateway['gateway']['m']:
								self.actor.data["m"] = gateway["gateway"]["m"]
								world.start_map(0)
						else:
							self.actor.data["h"] = gateway['gateway']['h']
							self.actor.data["m"] = -1
					else:
						# Move to x, y coordinate
						self.actor.data["x"] = dest_x
						self.actor.data["y"] = dest_y

class TStairAction(TMoveAction):
	def __init__(self, actor: TActor, direction: str):
		logger.debug(f"TStairAction->__init__( actor, direction={direction} )")
		super().__init__(actor, 0, 0)
		self.direction = direction

	"""
	def run(self):
		logger.debug(f"TStairAction->run()")
		world: TWorld = self.actor.world
		dest_x, dest_y = self.actor.current_xy
		map_idx = self.actor.map_idx
		if world.in_bounds(dest_x, dest_y, map_idx):
			map = self.actor.map
			# Check if walkable
			if map["tiles"]["walkable"][dest_x, dest_y]:
				gateway = world.go_gateway(dest_x, dest_y, map_idx, self.direction)
				if gateway is not None:
					# Move to x, y coordinate in map number m
					self.actor.data["x"] = gateway['gateway']["x"]
					self.actor.data["y"] = gateway['gateway']["y"]
					self.actor.data["m"] = gateway['gateway']["m"]
	"""