from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import colours as colour

if TYPE_CHECKING:
	from engine import TEngine
	from entity import TActor, TEntity

class TAction:
	def __init__(self, entity: TActor) -> None:
		super().__init__()
		self.entity = entity

	@property
	def engine(self) -> TEngine:
		"""Return the engine this action belongs to."""
		return self.entity.parent.engine

	def perform(self) -> None:
		"""Perform this action with the objects needed to determine its scope.

		`self.engine` is the scope this action is being performed in.

		`self.entity` is the object performing the action.

		This method must be overridden by Action subclasses.
		"""
		raise NotImplementedError()

class TEscapeAction(TAction):
	def perform(self) -> None:
		raise SystemExit()

class TWaitAction(TAction):
	def perform(self) -> None:
		pass

class TActionWithDirection(TAction):
	def __init__(self, entity: TActor, dx: int, dy: int):
		super().__init__(entity)

		self.dx = dx
		self.dy = dy

	@property
	def dest_xy(self) -> Tuple[int, int]:
		"""Returns this actions destination."""
		return self.entity.x + self.dx, self.entity.y + self.dy

	@property
	def blocking_entity(self) -> Optional[TEntity]:
		"""Return the blocking entity at this actions destination.."""
		return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

	@property
	def target_actor(self) -> Optional[TActor]:
		"""Return the actor at this actions destination."""
		return self.engine.game_map.get_actor_at_location(*self.dest_xy)

	def perform(self) -> None:
		raise NotImplementedError()

class TMeleeAction(TActionWithDirection):
	def perform(self) -> None:
		target = self.target_actor
		if not target:
			return  # No entity to attack.

		damage = self.entity.fighter.power - target.fighter.defense

		attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
		if self.entity is self.engine.player:
			attack_colour = colour.player_atk
		else:
			attack_colour = colour.enemy_atk

		if damage > 0:
			self.engine.message_log.add_message(f"{attack_desc} for {damage} hit points.", attack_colour)
			target.fighter.hp -= damage
		else:
			self.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_colour)

class TMovementAction(TActionWithDirection):
	def perform(self) -> None:
		dest_x, dest_y = self.dest_xy

		if not self.engine.game_map.in_bounds(dest_x, dest_y):
			return  # Destination is out of bounds.
		if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
			return  # Destination is blocked by a tile.
		if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
			return  # Destination is blocked by an entity.

		self.entity.move(self.dx, self.dy)

class TBumpAction(TActionWithDirection):
	def perform(self) -> None:
		if self.target_actor:
			return TMeleeAction(self.entity, self.dx, self.dy).perform()

		else:
			return TMovementAction(self.entity, self.dx, self.dy).perform()
