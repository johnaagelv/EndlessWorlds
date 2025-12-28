from __future__ import annotations

from typing import Final, Self
import client.g as g
import attrs
import tcod.ecs.callbacks
from tcod.ecs import Entity

from client.game.tags import IsWorld
#from client.game.world_tools import start_map

import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

@attrs.define(frozen=True)
class Position:
	""" Position of an entity """
	x: int # x coordinate of a position
	y: int # y coordinate of a position
	m: int # m coordinate of a position, which is the map

	def __add__(self, direction: tuple[int, int]) -> Self:
		""" Add vector to this position """
#		logger.debug(f"Position->__add__( {direction} ) -> Self")
		(world,) = g.game.Q.all_of(tags=[IsWorld])
		map = world.components[Maps].maps[self.m]
		x, y = direction
		new_x = self.x + x
		new_y = self.y + y
		new_m = self.m

		if 0 <= new_x < map["width"] and 0 <= new_y < map["height"] and map["tiles"][new_x, new_y]["walkable"]:
			pass
		else:
			new_x = self.x
			new_y = self.y
		return self.__class__(new_x, new_y, new_m)
	
@tcod.ecs.callbacks.register_component_changed(component=Position)
def on_position_changed(entity: Entity, old: Position | None, new: Position | None) -> None:
	""" Mirror position components as a tag """
#	logger.debug("on_position_changed( entity, old, new ) -> None")
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
	""" An entity face and colour """
	face: int = ord("!")
	colour: tuple[int, int, int] = (255, 255, 255)

StateName: Final = ("Name", str)
StateValue: Final = ("Value", int)
StateMax: Final = ("Max", int)
StateUsage: Final = ("Usage", int)
"""
Player states, such as Energy, Health, etc are implemented as:
- state_name, the name of this state
- state_value, the current value of this state
- state_max, max value of this state
- state_usage, how much usage per tick
"""

CID: Final = ("cid", str)

IsPlaying: Final = ("IsPlaying", bool)
""" Playing indicator """

Vision: Final = ("Vision", int)
""" Vision radius of an actor """

@attrs.define()
class World:
	""" World """
	definitions: list[dict] = []
	maps: list[dict] = []

@attrs.define()
class Maps:
	maps: list[dict] = []
	defs: list[dict] = []