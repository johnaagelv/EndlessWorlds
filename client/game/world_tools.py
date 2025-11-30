from __future__ import annotations

import numpy as np

from random import Random
#import tcod.console
from tcod.ecs import Registry
import client.tile_types as tile_types
import client.g as g
from client.game.components import Graphic, IsPlaying, Maps, Position, World, Vision, state_name, state_value, state_max, state_usage
from client.game.tags import IsActor, IsPlayer, IsState, IsWorld

import client.game.connect_tools

import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

def new_game() -> Registry:
#	logger.debug("new_world() -> Registry")
	game = Registry()

	rng = game[object()].components[Random] = Random()  # noqa: F841

	result = client.game.connect_tools.query_server(
		{
			"cmd": "new",
		}
	)

	map_sizes = result['map_sizes']
	map_template = {
		"loaded": bool,
		"width": int,
		"height": int,
		"tiles": np.ndarray,
		"visible": np.ndarray,
		"explored": np.ndarray,
		"gateways": list
	}
	map_template["loaded"] = False
#	logger.debug(f"- map sizes = {len(map_sizes)}")

	world = game[object()]
	world.components[World] = World()
	world.components[Maps] = Maps([map_template] * len(map_sizes), map_sizes)
	world.tags |= {IsWorld}

	player = game[object()]
	player.components[Position] = Position(result['entry_point'][0], result['entry_point'][1], result['entry_point'][3])
	player.components[Graphic] = Graphic(ord("@"))
	player.components[IsPlaying] = True
	player.tags |= {IsPlayer, IsActor}
	player.components[Vision] = 4

	for player_state in config.PLAYER_STATES:
		state = game[object()]
		state.components[state_name] = player_state[0]
		state.components[state_value] = player_state[1]
		state.components[state_max] = player_state[2]
		state.components[state_usage] = player_state[3]
		state.tags |= {IsState}

	return game

def start_map(map_idx: int) -> None:
#	logger.debug(f"start_map( map_idx {map_idx} ) -> None")
	(world,) = g.game.Q.all_of(tags=[IsWorld])
	maps = world.components[Maps]
#	logger.debug(f"- map {map_idx} keys: {maps.maps[map_idx].keys()}")
	if not maps.maps[map_idx]['loaded']:
		definition = maps.defs[map_idx]
#		logger.debug(f"- def: {definition}")
		map_width = int(definition["width"])
		map_height = int(definition["height"])
		map_visible = definition["visible"]
		maps.maps[map_idx] = {
			"loaded": True,
			"name": definition["name"],
			"width": map_width,
			"height": map_height,
			"gateways": definition["gateways"],
			"tiles": np.full((map_width, map_height), fill_value=tile_types.blank, order="F"),
			"visible": np.full((map_width, map_height), fill_value=map_visible, order="F"),
			"explored": np.full((map_width, map_height), fill_value=map_visible, order="F"),
		}

		if map_visible:
#			logger.debug(f"- visible map {map_idx}")
			fos: dict = definition["fos"]
			temp = fos.get("view")
			view = np.array(temp)
			maps.maps[map_idx]["tiles"][0:map_width, 0:map_height] = view

def in_gateway(x: int, y: int, map_idx: int) -> bool:
#	logger.debug(f"in_gateway( x={x}, y={y}, m={map_idx} )")
	(world,) = g.game.Q.all_of(tags=[IsWorld])
	maps = world.components[Maps]
#	logger.debug(f"- tile({x},{y}): {maps.maps[map_idx]['tiles'][x, y]}")
	return maps.maps[map_idx]["tiles"][x, y]["gateway"]

def go_gateway(x: int, y: int, map_idx: int, direction = None) -> dict:
#	logger.debug(f"go_gateway( x={x}, y={y}, m={map_idx}, direction={direction} )")
	(world,) = g.game.Q.all_of(tags=[IsWorld])
	maps = world.components[Maps]
	gateway_fallback = {
		"gateway": {
			"x": x,
			"y": y,
			"m": map_idx,
			"h": ""
		}
	}
	if direction is None:
		gateway = next((item for item in maps.maps[map_idx]["gateways"] if item["x"] == x and item["y"] == y), gateway_fallback)
	else:
		gateway = next((item for item in maps.maps[map_idx]["gateways"] if item["x"] == x and item["y"] == y and item['action'] == direction), gateway_fallback)
	return gateway

def get_view_port(pos: Position) -> tuple:
	""" Calculate the view port """
	(world,) = g.game.Q.all_of(tags=[IsWorld])
	maps = world.components[Maps]

	view_width = config.VIEW_PORT_WIDTH
	view_height = config.VIEW_PORT_HEIGHT

	width = maps.maps[pos.m]["width"]
	height = maps.maps[pos.m]["height"]

	view_x1 = min(max(0, pos.x - int(view_width / 2)), width - view_width)
	view_x2 = view_x1 + view_width

	view_y1 = min(max(0, pos.y - int(view_height / 2)), height - view_height)
	view_y2 = view_y1 + view_height
	return (view_x1, view_x2, view_y1, view_y2)

#def get_entities_at_location(self, location_x: int, location_y: int) -> Optional[List]:
#	return [entity for entity in self.entities if entity.data['x'] == location_x and entity.data['y'] == location_y]
