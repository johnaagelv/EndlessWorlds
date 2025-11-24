from __future__ import annotations

import numpy as np
import client.tile_types as tile_types
from typing import Final, Self
import client.g as g
import attrs
import tcod.ecs.callbacks
from tcod.ecs import Entity

from client.game.tags import IsPlayer, IsWorld

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
		logger.debug(f"Position->__add__( {direction} ) -> Self")
		(world,) = g.game.Q.all_of(tags=[IsWorld])
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
#		map_idx = player.components[Map]
		map = world.components[World].maps[self.m]
		x, y = direction
		new_x = self.x + x
		new_y = self.y + y
		if map["tiles"][new_x, new_y]["walkable"] and 0 <= new_x < map["width"] and 0 <= new_y < map["height"]:
			pass
		else:
			new_x = self.x
			new_y = self.y

		return self.__class__(new_x, new_y, self.m)
	
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
	definitions: list[dict] = []
	maps: list[dict] = []

	def start_map(self, map_idx: int) -> None:
		logger.debug("World->start_map( map_idx ) -> None")
		if not self.maps[map_idx]['loaded']:
			map_definition: dict = self.definitions[map_idx]

			map_width = int(map_definition["width"])
			map_height = int(map_definition["height"])
			map_visible = map_definition["visible"]
			self.maps[map_idx] = {
				"loaded": True,
				"name": map_definition["name"],
				"width": map_width,
				"height": map_height,
				"tiles": np.full((map_width, map_height), fill_value=tile_types.blank, order="F"),
				"visible": np.full((map_width, map_height), fill_value=map_visible, order="F"),
				"explored": np.full((map_width, map_height), fill_value=map_visible, order="F"),
			}

			if map_visible:
				fos: dict = map_definition["fos"]
				temp = fos.get("view")
				view = np.array(temp)
				self.maps[map_idx]["tiles"][0:map_width, 0:map_height] = view

	def render(self, map_idx, console: tcod.console.Console, view_port: tuple) -> None:
		logger.debug(f"World->render( map_idx {map_idx}, console )")

		visible_tiles = self.maps[map_idx]['visible']
		explored_tiles = self.maps[map_idx]['explored']
		light_tiles = self.maps[map_idx]['tiles']['light']
		dark_tiles = self.maps[map_idx]['tiles']['dark']

		view_x1, view_x2, view_y1, view_y2 = view_port

		console.rgb[0:config.VIEW_PORT_WIDTH, 0:config.VIEW_PORT_HEIGHT] = np.select(
			condlist=[visible_tiles[view_x1:view_x2, view_y1:view_y2], explored_tiles[view_x1:view_x2, view_y1:view_y2]],
			choicelist=[light_tiles[view_x1:view_x2, view_y1:view_y2], dark_tiles[view_x1:view_x2, view_y1:view_y2]],
			default=tile_types.SHROUD
		)

	def in_gateway(self, x: int, y: int, m: int) -> bool:
		logger.debug(f"World->in_gateway( x={x}, y={y}, m={m} )")
		return self.maps[m]["tiles"][x, y]["gateway"]

	def go_gateway(self, x: int, y: int, m: int, direction = None) -> dict:
		logger.debug(f"TWorld->go_gateway( x={x}, y={y}, m={m}, direction={direction} )")
		gateway_fallback = {
			"gateway": {
				"x": x,
				"y": y,
				"m": m,
				"h": ""
			}
		}
		if direction is None:
			gateway = next((item for item in self.maps[m]["gateways"] if item["x"] == x and item["y"] == y), gateway_fallback)
		else:
			gateway = next((item for item in self.maps[m]["gateways"] if item["x"] == x and item["y"] == y and item['action'] == direction), gateway_fallback)
		return gateway
