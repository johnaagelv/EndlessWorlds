from __future__ import annotations

import random
from typing import List, Optional, Tuple, TYPE_CHECKING

import numpy as np  # type: ignore
import tcod

from actions import TAction, TBumpAction, TMeleeAction, TMovementAction, TWaitAction
import colours as colour

if TYPE_CHECKING:
	from entity import TActor

class TBaseAI(TAction):
	entity: TActor

	def perform(self) -> None:
		raise NotImplementedError()

	def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
		"""Compute and return a path to the target position.

		If there is no valid path then returns an empty list.
		"""
		# Copy the walkable array.
		cost = np.array(self.entity.parent.tiles["walkable"], dtype=np.int8)

		for entity in self.entity.parent.entities:
			# Check that an enitiy blocks movement and the cost isn't zero (blocking.)
			if entity.blocks_movement and cost[entity.x, entity.y]:
				# Add to the cost of a blocked position.
				# A lower number means more enemies will crowd behind each other in
				# hallways.  A higher number means enemies will take longer paths in
				# order to surround the player.
				cost[entity.x, entity.y] += 10

		# Create a graph from the cost array and pass that graph to a new pathfinder.
		graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
		pathfinder = tcod.path.Pathfinder(graph)

		pathfinder.add_root((self.entity.x, self.entity.y))  # Start position.

		# Compute the path to the destination and remove the starting point.
		path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

		# Convert from List[List[int]] to List[Tuple[int, int]].
		return [(index[0], index[1]) for index in path]


class THostileEnemy(TBaseAI):
	def __init__(self, entity: TActor):
		super().__init__(entity)
		self.path: List[Tuple[int, int]] = []

	def perform(self) -> None:
		target = self.engine.player
		dx = target.x - self.entity.x
		dy = target.y - self.entity.y
		distance = max(abs(dx), abs(dy))  # Chebyshev distance.
		move_chance = random.random() < 0.005 
		if self.engine.game_world.maps[self.engine.game_world.current_floor].visible[self.entity.x, self.entity.y] or move_chance:
			if distance <= 1:
				return TMeleeAction(self.entity, dx, dy).perform()

			self.path = self.get_path_to(target.x, target.y)

		if self.path:
			dest_x, dest_y = self.path.pop(0)

			path_steps = len(self.path)
			if move_chance and path_steps > 8 and path_steps < 32:
				self.engine.message_log.add_message(f"You hear movement!", colour.sound_of_movement)
				self.path = []

			return TMovementAction(
				self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
			).perform()
		
		return TWaitAction(self.entity).perform()

class TConfusedEnemy(TBaseAI):
	"""
	A confused enemy will stumble around aimlessly for a given number of turns,
	then revert back to its previous AI. If an actor occupies a tile it is randomly
	moving into, it will attack
	"""
	def __init__(self, entity: TActor, previous_ai: Optional[TBaseAI], turns_remaining: int):
		super().__init__(entity)
		self.previous_ai = previous_ai
		self.turns_remaining = turns_remaining
	
	def perform(self) -> None:
		if self.turns_remaining <= 0:
			self.engine.message_log.add_message(
				f"The {self.entity.name} is no longer confused!"
			)
			self.entity.ai = self.previous_ai
		else:
			direction_x, direction_y = random.choice(
				[
					(-1, -1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)
				]
			)
			self.turns_remaining -= 1

			# Actor will either try to move or attack in the chosen direction
			# Its possible the actor will just bump into the wall, wasting a turn
			return TBumpAction(self.entity, direction_x, direction_y,).perform()