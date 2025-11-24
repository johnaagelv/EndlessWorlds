from __future__ import annotations

import numpy as np

from random import Random
from tcod.ecs import Registry
from client.game.components import Energy, Graphic, Health, IsPlaying, Position, World, Vision
from client.game.tags import IsActor, IsPlayer, IsWorld

import client.game.connect_tools

import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

def new_game() -> Registry:
	logger.debug("new_world() -> Registry")
	game = Registry()

	rng = game[object()].components[Random] = Random()  # noqa: F841

	world = game[object()]
	world.components[World] = World()
	world.tags |= {IsWorld}

	result = client.game.connect_tools.query_server(
		{
			"cmd": "new",
#			"cid": "1234",
#			"x": 10,
#			"y": 10,
#			"z": 0,
#			"m": 2,
#			"r": 4,
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
	logger.debug(f"- map sizes = {len(map_sizes)}")
	world.components[World].maps = [map_template] * len(map_sizes)
	world.components[World].definitions = map_sizes

#	logger.debug(f"{world.components[World].maps[2]}")

	player = game[object()]
	player.components[Position] = Position(result['entry_point'][0], result['entry_point'][1], result['entry_point'][3])
	player.components[Graphic] = Graphic(ord("@"))
	player.components[Health] = 500
	player.components[Energy] = 500
	player.components[IsPlaying] = True
	player.tags |= {IsPlayer, IsActor}

	player.components[Vision] = 4

	return game

def load_worlds() -> list[dict]:
	items = [
		{"name": "Demo", "ip": "192.168.1.104:25261"},
		{"name": "Ankt", "ip": "192.168.1.104:54321"},
	]
	return items

def load_world() -> None:
	logger.debug("load_world() -> None")

