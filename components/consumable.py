from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import colours as colour
import components.ai
from components.inventory import TInventory
from components.base_component import TBaseComponent
from exceptions import Impossible
from input_handlers import TAreaRangedAttachHandler, TSingleRangedAttackHandler

if TYPE_CHECKING:
	from entity import TActor, TItem

class TConsumable(TBaseComponent):
	parent: TItem

	def get_action(self, consumer: TActor) -> Optional[actions.TAction]:
		return actions.TItemAction(consumer, self.parent)
	
	def activate(self, action: actions.TItemAction) -> None:
		raise NotImplementedError()
	
	def consume(self) -> None:
		"""
		Remove the consumed item from its containing inventory
		"""
		entity = self.parent
		inventory = entity.parent
		if isinstance(inventory, TInventory):
			inventory.items.remove(entity)

class TConfusionConsumable(TConsumable):
	def __init__(self, number_of_turns: int):
		self.number_of_turns = number_of_turns

	def get_action(self, consumer: TActor) -> Optional[actions.TAction]:
		self.engine.message_log.add_message("Select a target location!", colour.needs_target)
		self.engine.event_handler = TSingleRangedAttackHandler(
			self.engine,
			callback=lambda xy: actions.TItemAction(consumer, self.parent, xy),
		)
		return None
	
	def activate(self, action: actions.TItemAction) -> None:
		consumer = action.entity
		target = action.target_actor
		if not self.engine.game_map.visible[action.target_xy]:
			raise Impossible("You cannot target this area!")
		if not target:
			raise Impossible("You must select a target!")
		if target is consumer:
			raise Impossible("You target yourself!")
		
		self.engine.message_log.add_message(
			f"The eyes of the {target.name} look vacant, as it starts to stumble around",
			colour.status_effect_applied
		)
		target.ai = components.ai.TConfusedEnemy(
			entity=target, previous_ai=target.ai, turns_remaining=self.number_of_turns,
		)
		self.consume()
	
class THealingConsumable(TConsumable):
	def __init__(self, amount: int):
		self.amount = amount
	
	def activate(self, action: actions.TItemAction) -> None:
		consumer = action.entity
		amount_recovered = consumer.fighter.heal(self.amount)

		if amount_recovered > 0:
			self.engine.message_log.add_message(
				f"You consume the {self.parent.name}, and recover {amount_recovered} HP!",
				colour.health_recovered
			)
			self.consume()
		else:
			raise Impossible(f"You health is already at max!")

class TLightningDamageConsumable(TConsumable):
	def __init__(self, damage: int, maximum_range: int):
		self.damage = damage
		self.maximum_range = maximum_range
	
	def activate(self, action: actions.TItemAction) -> None:
		consumer = action.entity
		target = None
		closest_distance = self.maximum_range + 1.0
	
		for actor in self.engine.game_map.actors:
			if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
				distance = consumer.distance(actor.x, actor.y)

				if distance < closest_distance:
					target = actor
					closest_distance = distance
		
		if target:
			self.engine.message_log.add_message(
				f"A lighting bolt strikes the {target.name} with a loud thunder, for {self.damage} damage!"
			)
			target.fighter.take_damage(self.damage)
			self.consume()
		else:
			raise Impossible("None in range!")

class TFireballDamageConsumable(TConsumable):
	def __init__(self, damage: int, radius: int):
		self.damage = damage
		self.radius = radius
	
	def get_action(self, consumer: TActor) -> Optional[actions.TAction]:
		self.engine.message_log.add_message("Select target location", colour.needs_target)
		self.engine.event_handler = TAreaRangedAttachHandler(
			self.engine,
			radius=self.radius,
			callback=lambda xy: actions.TItemAction(consumer, self.parent, xy)
		)
		return None

	def activate(self, action: actions.TItemAction) -> None:
		target_xy = action.target_xy

		if not self.engine.game_map.visible[target_xy]:
			raise Impossible("Out of range!")
		
		targets_hit = False
		for actor in self.engine.game_map.actors:
			if actor.distance(*target_xy) <= self.radius:
				self.engine.message_log.add_message(
					f"Fire engulfs {actor.name}!"
				)
				actor.fighter.take_damage(self.damage)
				targets_hit = True
		
		if not targets_hit:
			raise Impossible("No targets hit!")
		self.consume()