""" This module contains all components """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

from typing import Final, List, Self

import attrs
import tcod.ecs.callbacks
from tcod.ecs import Entity, Registry
import numpy as np
import g
from game.tags import IsPlayer

""" Is a """
@attrs.define(frozen=True)
class IsA:
	stats: object

""" Base container """
@attrs.define(frozen=False)
class BaseContainer:
	registry: object
	slots: int # Number of items this container can contain
	# weight: int # Max weight of all items that this container can contain

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
	def __add__(self, value: int) -> Self:
		return self.__class__(max(0, self.value + value))

""" Water ... """
class WaterPouch(BaseItem):
	...

""" Amount of gold """
class Gold(BaseItem):
	...

""" Food parcels """
class Food(BaseItem):
	...

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
