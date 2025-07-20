""" World tools to manage the ECS registry """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

from random import Random
from tcod.ecs import Registry
from game.components import Explored, Graphic, Gold, ExplorationMemory, Position, Visible, World
from game.tags import IsActor, IsItem, IsPlayer

import numpy as np
import tile_types

def new_world() -> Registry:
	logger.info("new_world() -> Registry")
	registry = Registry()

	""" Register a random number generator """
	rng = registry[None].components[Random] = Random()

	world = registry[object()]

	player = registry[object()]
	player.components[Position] = Position(5, 5)
	player.components[Graphic] = Graphic(ord("@"))
	player.components[Gold] = 0
	player.tags |= {IsPlayer, IsActor}

	world.components[ExplorationMemory] = ExplorationMemory(
		np.full((80, 50), fill_value=tile_types.blank, order="F"),
		np.full((80, 50), fill_value=False, order="F"),
		np.full((80, 50), fill_value=False, order="F"),
		[]
	)

	for _ in range(rng.randint(6,12)):
		valuable = registry[object()]
		valuable.components[Position] = Position(rng.randint(0, 10), rng.randint(0, 25))
		valuable.components[Graphic] = Graphic(ord("$"), fg=(255, 255, 0))
		valuable.components[Gold] = rng.randint(1, 10)
		valuable.tags |= {IsItem}

	return registry