from __future__ import annotations

from typing import TYPE_CHECKING

import colours as colour

from components.base_component import BaseComponent
from input_handlers import TGameOverEventHandler
from render_order import RenderOrder

if TYPE_CHECKING:
	from entity import TActor


class TFighter(BaseComponent):
	entity: TActor

	def __init__(self, hp: int, defense: int, power: int):
		self.max_hp = hp
		self._hp = hp
		self.defense = defense
		self.power = power

	@property
	def hp(self) -> int:
		return self._hp

	@hp.setter
	def hp(self, value: int) -> None:
		self._hp = max(0, min(value, self.max_hp))
		if self._hp == 0 and self.entity.ai:
			self.die()

	def die(self) -> None:
		if self.engine.player is self.entity:
			death_message = "You died!"
			death_message_colour = colour.player_die
			self.engine.event_handler = TGameOverEventHandler(self.engine)
		else:
			death_message = f"{self.entity.name} is dead!"
			death_message_colour = colour.enemy_die

		self.entity.char = "%"
		self.entity.color = (191, 0, 0)
		self.entity.blocks_movement = False
		self.entity.ai = None
		self.entity.name = f"remains of {self.entity.name}"
		self.entity.render_order = RenderOrder.CORPSE

		self.engine.message_log.add_message(death_message, death_message_colour)