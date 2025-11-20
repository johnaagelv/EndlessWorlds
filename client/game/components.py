from __future__ import annotations

from typing import Final, Self

import attrs
import tcod.ecs.callbacks
from tcod.ecs import Entity

import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

@attrs.define(frozen=True)
class Position:
	""" Position of an entity """
	x: int # x coordinate of a position
	y: int # y coordinate of a position

	def __add__(self, direction: tuple[int, int]) -> Self:
		""" Add vector to this position """
		logger.debug("Position->__add__( direction ) -> Self")
		x, y = direction
		return self.__class__(self.x + x, self.y + y)
	
@tcod.ecs.callbacks.register_component_changed(component=Position)
def on_position_changed(entity: Entity, old: Position | None, new: Position | None) -> None:
	""" Mirror position components as a tag """
	logger.debug("on_position_changed( entity, old, new ) -> None")
	if old == new:
		# Position was not changed, so discard change
		return
	if old is not None:
		# Remove old position
		entity.tags.discard(old)
	if new is not None:
		# Add new position
		entity.tags.add(new)

@attrs.define(frozen=True)
class Graphic:
	""" An entities face and colour """
	face: int = ord("!")
	colour: tuple[int, int, int] = (255, 255, 255)

Health: Final = ("Health", int)
""" Amount of health """

Energy: Final = ("Energy", int)
""" Amount of energy """

IsPlaying: Final = ("IsPlaying", bool)
""" Playing indicator """

Map: Final = ("Map", int)
""" Map index of current position of an entity """

Vision: Final = ("Vision", int)
""" Vision radius of an actor """

@attrs.define()
class World:
	""" World """
	maps: list[dict] = []