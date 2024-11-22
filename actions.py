from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import colours as colour
import exceptions

if TYPE_CHECKING:
	from engine import TEngine
	from entity import TActor, TEntity, TItem

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

class TPickupAction(TAction):
	"""
	Pickup an item and add it to the inventory
	"""
	def __init__(self, entity: TActor):
		super().__init__(entity)
	
	def perform(self) -> None:
		actor_location_x = self.entity.x
		actor_location_y = self.entity.y
		inventory =self.entity.inventory

		for item in self.engine.game_map.items:
			if actor_location_x == item.x and actor_location_y == item.y:
				if len(inventory.items) >= inventory.capacity:
					raise exceptions.Impossible("Your inventory is full!")
				
				self.engine.game_map.entities.remove(item)
				item.parent = self.entity.inventory
				inventory.items.append(item)

				self.engine.message_log.add_message(f"You picked up the {item.name}!")
				return

		raise exceptions.Impossible("There is nothing here to pick up!")

class TItemAction(TAction):
	def __init__(self, entity: TActor, item: TItem, target_xy: Optional[Tuple[int, int]]=None):
		super().__init__(entity)
		self.item = item
		if not target_xy:
			target_xy = entity.x, entity.y
		self.target_xy = target_xy
	
	@property
	def target_actor(self) -> Optional[TActor]:
		"""
		Return the actor at this actions destination
		"""
		return self.engine.game_map.get_actor_at_location(*self.target_xy)
	
	def perform(self) -> None:
		"""
		Invoke the items ability, this action will be given to provide context
		"""
		self.item.consumable.activate(self)

class TDropItem(TItemAction):
	def perform(self) -> None:
		self.entity.inventory.drop(self.item)

class TWaitAction(TAction):
	def perform(self) -> None:
		pass

class TTakeDownStairsAction(TAction):
	def perform(self) -> None:
		"""
		Take the stairs
		"""
		if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
			self.engine.game_world.descend_floor()
			self.engine.message_log.add_message(f"You go down! {self.engine.game_world.current_floor}", colour.descend)
		else:
			raise exceptions.Impossible("Doh!")

class TTakeUpStairsAction(TAction):
	def perform(self) -> None:
		"""
		Take the stairs
		"""
		if (self.entity.x, self.entity.y) == self.engine.game_map.upstairs_location:
			self.engine.game_world.ascend_floor()
			self.engine.message_log.add_message(f"You go up! {self.engine.game_world.current_floor}", colour.descend)
		else:
			raise exceptions.Impossible("Doh!")

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
			raise exceptions.Impossible("Nothing to attack!")

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
			raise exceptions.Impossible("The way is blocked!")
		if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
			raise exceptions.Impossible("Ouch!")
		if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
			raise exceptions.Impossible("Watch where you're going!")

		self.entity.move(self.dx, self.dy)

class TBumpAction(TActionWithDirection):
	def perform(self) -> None:
		if self.target_actor:
			return TMeleeAction(self.entity, self.dx, self.dy).perform()

		else:
			return TMovementAction(self.entity, self.dx, self.dy).perform()
