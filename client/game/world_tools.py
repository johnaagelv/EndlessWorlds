from __future__ import annotations

from random import Random
from tcod.ecs import Registry
from client.game.components import Energy, Graphic, Health, IsPlaying, Position, World, Map, Vision
from client.game.tags import IsActor, IsPlayer, IsWorld

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
	
	player = game[object()]
	player.components[Position] = Position(5, 5)
	player.components[Graphic] = Graphic(ord("@"))
	player.components[Health] = 500
	player.components[Energy] = 500
	player.components[IsPlaying] = True
	player.tags |= {IsPlayer, IsActor}

	player.components[Map] = 0
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
	