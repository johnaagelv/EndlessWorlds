from __future__ import annotations

from typing import Final, Self

import attrs
import tcod.ecs.callbacks
from tcod.ecs import Entity

@attrs.define(frozen=True)
class Position:
	""" Position of an entity """
	x: int
	y: int

	def __add__(self, direction: tuple[int, int]) -> Self:
		""" Add vector to this position """
		x, y = direction
		return self.__class__(self.x + x, self.y + y)
	
@tcod.ecs.callbacks.register_component_changed(component=Position)
def on_position_changed(entity: Entity, old: Position | None, new: Position | None) -> None:
	""" Mirror position components as a tag """
	if old == new:
		return
	if old is not None:
		entity.tags.discard(old)
	if new is not None:
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
