from __future__ import annotations

from components.components import TBaseComponent

class TFighter(TBaseComponent):
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