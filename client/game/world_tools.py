from __future__ import annotations

from random import Random
from tcod.ecs import Registry
from client.game.components import Energy, Graphic, Health, IsPlaying, Position
from client.game.tags import IsActor, IsPlayer

import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

def new_world() -> Registry:
	logger.debug("new_world() -> Registry")
	world = Registry()
	rng = world[object()].components[Random] = Random()  # noqa: F841
	player = world[object()]
	player.components[Position] = Position(5, 5)
	player.components[Graphic] = Graphic(ord("@"))
	player.components[Health] = 500
	player.components[Energy] = 500
	player.components[IsPlaying] = True
	player.tags |= {IsPlayer, IsActor}

	return world