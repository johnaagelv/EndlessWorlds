from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import colours as colour
from components.inventory import TInventory
from components.base_component import TBaseComponent
from exceptions import Impossible

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