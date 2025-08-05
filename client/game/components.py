""" This module contains all components """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

import time
from typing import Final, List, Reversible, Self, Tuple
import textwrap
import attrs
import tcod.ecs.callbacks
from tcod.ecs import Entity, Registry
import numpy as np
import g
from game.tags import IsPlayer
import colours

""" Is a """
@attrs.define(frozen=True)
class IsA:
	name: str

""" Base container """
@attrs.define(frozen=False)
class BaseContainer:
	registry: Registry
	slots: int # Number of items this container can contain
	#weight: int # Max weight of all items that this container can contain

""" Inventory """
class Inventory(BaseContainer):
	...

""" Equipment """
class Equipment(BaseContainer):
	...

""" Backpack """
class BackPack(BaseContainer):
	...

""" Tools belt """
class Toolsbelt(BaseContainer):
	...

""" Base item class """
@attrs.define(frozen=False)
class BaseItem:
	value: int # Usually 1 but gold, arrows, ammunition, and consumables may be larger
	name: str | None
	def __add__(self, value: int) -> Self:
		return self.__class__(max(0, self.value + value), self.name)

""" Water ... """
class WaterPouch(BaseItem):
	...

""" Amount of gold """
class Gold(BaseItem):
	...

""" Food parcels """
class Food(BaseItem):
	...

#FoodParcel : Final = ("Food", int)

""" Map memory of an entity """
@attrs.define(frozen=False)
class ExplorationMemory:
	map: np.ndarray
	visible: np.ndarray
	explored: np.ndarray
	gateways: List

""" Map memory of an entity """
@attrs.define(frozen=False)
class Map:
	map: np.ndarray
	visible: np.ndarray
	explored: np.ndarray
	gateways: List

""" Position of an entity """
@attrs.define(frozen=True)
class Position:
	x: int # X coordinate of the player on the map
	y: int # Y coordinate of the player on the map

	def __add__(self, direction: tuple[int, int]) -> Self:
		logger.info("Position->__add__( direction ) -> Self")
		""" Add a direction vector to this position """
		x, y = direction
		return self.__class__(self.x + x, self.y + y)

""" Mirror position components as tags """
@tcod.ecs.callbacks.register_component_changed(component=Position)
def on_position_changed(entity: Entity, old: Position | None, new: Position | None) -> None:
	logger.info("on_position_changed( entity, old, new ) -> None")
	if old == new:
		return
	if old is not None:
		entity.tags.discard(old)
	if new is not None:
		entity.tags.add(new)

""" Icon and colour of an entity """
@attrs.define(frozen=True)
class Graphic:
	ch: int = ord("!")
	fg: tuple[int, int, int] = (255, 255, 255)


""" Input is processed by an entity """
@attrs.define(frozen=False)
class Input:
	sym: tcod.event.KeySym

""" Health of the entity (0 - 1000000) """
@attrs.define(frozen=True)
class Health:
	value: int
	low: int	# 0-low, stats goes red
	medium: int	# low-medium, stats goes orange
	high: int 	# medium-high+, stats goes green
	def __add__(self, value: int) -> Self:
		logger.info("Health->__add__( value ) -> Self")
		return self.__class__(max(0, self.value + value), self.low, self.medium, self.high)

""" Health limits that affects other abilities (strength, ...) """
@attrs.define(frozen=False)
class HealthImpacts:
	low: int	# 100000
	medium: int	# 200000
	high: int 	# 300000
	impacts: List

""" Mirror Health components as tags """
@tcod.ecs.callbacks.register_component_changed(component=Health)
def on_health_changed(entity: Entity, old: Health | None, new: Health | None) -> None:
	logger.info("on_health_changed( entity, old, new ) -> None")
	if old == new:
		return
	if old is not None:
		entity.tags.discard(old)
	if new is not None:
		entity.tags.add(new)

""" Energy of the entity (0 - 1000000) """
@attrs.define(frozen=True)
class Energy:
	value: int
	low: int		# 50000
	medium: int	# 100000
	high: int 	# 150000
	def __add__(self, value: int) -> Self:
		logger.info("Energy->__add__( value ) -> Self")
		return self.__class__(max(0, self.value + value), self.low, self.medium, self.high)

""" Energy used per game tick """
@attrs.define(frozen=False)
class EnergyUsage:
	value: int

""" Stats impact on other abilities (health, strength, ...) """
@attrs.define(frozen=False)
class EnergyImpacts:
	low: int	# -100
	medium: int	# -50
	high: int 	# -1
	impacts: List # Other components affected by these limits

""" Stats impact on other abilities (health, strength, ...) """
@attrs.define(frozen=False)
class StatsImpacts:
	impacts: List # Other components affected

""" Mirror Energy components as tags """
@tcod.ecs.callbacks.register_component_changed(component=Energy)
def on_energy_changed(entity: Entity, old: Energy | None, new: Energy | None) -> None:
	logger.info("on_energy_changed( entity, old, new ) -> None")
	if old == new:
		return
	if old is not None:
		entity.tags.discard(old)
	if new is not None:
		entity.tags.add(new)

@attrs.define(frozen=False)
class Strength:
	value: int
	low: int	# 50000
	medium: int	# 100000
	high: int 	# 150000
	def __add__(self, value: int) -> Self:
		logger.info("Strength->__add__( value ) -> Self")
		return self.__class__(max(0, self.value + value), self.low, self.medium, self.high)

@attrs.define(frozen=False)
class StrengthImpacts:
	low: int
	medium: int
	high: int
	impacts: List

""" Message for one action performed in the game by the player """
class Message:
	def __init__(self, text: str, fg: Tuple[int, int, int]):
		self.plain_text = text
		self.fg = fg
		self.count = 1

	@property
	def full_text(self) -> str:
		if self.count > 1:
			return f"{self.plain_text} (x{self.count})"
		return self.plain_text

""" MessageLog to keep track of all actions performed in the game by the player """
class MessageLog:
	def __init__(self) -> None:
		self.messages: List[Message] = []
	
	""" Add a message to the message log """
	def add(self, text: str, fg: Tuple[int, int, int] = colours.white, *, stack: bool = True) -> None:
		if stack and self.messages and text == self.messages[-1].plain_text:
			self.messages[-1].count += 1
		else:
			self.messages.append(Message(text, fg))

	""" Render the messages that can fit within the specified window size """
	def render(self, console: tcod.console.Console, x: int, y: int, width: int, height: int) -> None:
		self.render_messages(console, x, y, width, height, self.messages)

	""" Render all the messages that can fit within the specified window size """
	@staticmethod
	def render_messages(console: tcod.console.Console, x: int, y: int, width: int, height: int, messages: Reversible[Message]) -> None:
		y_offset = height - 1
		for message in reversed(messages):
			for line in reversed(textwrap.wrap(message.full_text, width)):
				console.print(x=x, y=y+y_offset, text=line, fg=message.fg)
				y_offset -= 1
				if y_offset < 0:
					return

	""" Empty the message log """
	def clear(self) -> None:
		self.messages = []
		return None

@attrs.define(frozen=False)
class Relationship:
	item: tcod.ecs.Entity
	value: int # bad > normal > good

@attrs.define(frozen=False)
class TargetPosition:
	x: int
	y: int

@attrs.define(frozen=False)
class ActorTimer:
	start_time: float
	