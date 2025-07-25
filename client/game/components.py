""" This module contains all components """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

from typing import Final, List, Self

import attrs
import tcod.ecs.callbacks
from tcod.ecs import Entity, Registry
import numpy as np

""" World registry """
@attrs.define(frozen=False)
class World:
	registry: Registry

""" Map memory of an entity """
@attrs.define(frozen=False)
class ExplorationMemory:
	map: np.ndarray
	visible: np.ndarray
	explored: np.ndarray
	gateways: List

""" Map parts visible by entity's Field of Sense """
@attrs.define(frozen=False)
class Visible:
	visible: np.ndarray

""" Map parts explored by entity """
@attrs.define(frozen=False)
class Explored:
	explored: np.ndarray

""" Position of an entity """
@attrs.define(frozen=True)
class Position:
	x: int # X coordinate of the player on the map
	y: int # Y coordinate of the player on the map
	# z: int # Height of the player on the map
	# m: int # Map of the world

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

""" Amount of gold """
Gold: Final = ("Gold", int)
