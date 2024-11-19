from __future__ import annotations

from typing import List, TYPE_CHECKING

from components.base_component import TBaseComponent

if TYPE_CHECKING:
	from entity import TActor, TItem

class TInventory(TBaseComponent):
	parent: TActor
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.items: List[TItem] = []
	
	def drop(self, item: TItem) -> None:
		"""
		Removes an item from the inventory and restores it to the game map,
		at the player's position
		"""
		self.items.remove(item)
		item.place(self.parent.x, self.parent.y, self.gamemap)
		self.engine.message_log.add_message(f"You dropped the {item.name}")