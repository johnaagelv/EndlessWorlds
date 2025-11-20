from __future__ import annotations

from random import Random
from tcod.ecs import Registry
from client.game.components import Energy, Graphic, Health, IsPlaying, Position, World
from client.game.tags import IsActor, IsPlayer

import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

def new_game() -> Registry:
	logger.debug("new_world() -> Registry")
	game = Registry()

	rng = game[object()].components[Random] = Random()  # noqa: F841

	world = game[object()]
	world.components[World] = World()
	
	player = game[object()]
	player.components[Position] = Position(5, 5)
	player.components[Graphic] = Graphic(ord("@"))
	player.components[Health] = 500
	player.components[Energy] = 500
	player.components[IsPlaying] = True
	player.tags |= {IsPlayer, IsActor}

	return game

def load_world() -> None:
	logger.debug("load_world() -> None")
	