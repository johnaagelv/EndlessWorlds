""" World tools to manage the ECS registry """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

from random import Random
from tcod.ecs import Registry
from game.components import Graphic, Gold, Map, Position, Silver
from game.tags import IsActor, IsItem, IsPlayer

import numpy as np
import tile_types

def new_world() -> Registry:
	logger.info("new_world() -> Registry")
	world = Registry()

	""" Register a random number generator """
	rng = world[None].components[Random] = Random()

	player = world[object()]
	player.components[Position] = Position(5, 5)
	player.components[Graphic] = Graphic(ord("@"))
	player.components[Gold] = 0
	player.components[Silver] = 0
	player.tags |= {IsPlayer, IsActor}
	player.components[Map] = Map(np.full((80, 50), fill_value=tile_types.blank, order="F"))

	for _ in range(rng.randint(6,12)):
		valuable = world[object()]
		valuable.components[Position] = Position(rng.randint(0, 80), rng.randint(0, 45))
		valuable.components[Graphic] = Graphic(ord("$"), fg=(255, 255, 0))
		valuable.components[Gold] = rng.randint(1, 10)
		valuable.tags |= {IsItem}

	for _ in range(rng.randint(8,20)):
		valuable = world[object()]
		valuable.components[Position] = Position(rng.randint(0, 80), rng.randint(0, 45))
		valuable.components[Graphic] = Graphic(ord("$"), fg=(192, 192, 192))
		valuable.components[Silver] = rng.randint(1, 10)
		valuable.tags |= {IsItem}

	return world