""" World tools to manage the ECS registry """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

from random import Random
from tcod.ecs import Registry
from game.components import Graphic, Gold, Position
from game.tags import IsActor, IsItem, IsPlayer

def new_world() -> Registry:
	logger.info("new_world() -> Registry")
	world = Registry()

	""" Register a random number generator """
	rng = world[None].components[Random] = Random()

	player = world[object()]
	player.components[Position] = Position(5, 5)
	player.components[Graphic] = Graphic(ord("@"))
	player.components[Gold] = 1
	player.tags |= {IsPlayer, IsActor}

	for _ in range(10):
		gold = world[object()]
		gold.components[Position] = Position(rng.randint(0, 20), rng.randint(0, 20))
		gold.components[Graphic] = Graphic(ord("$"), fg=(255, 255, 0))
		gold.components[Gold] = rng.randint(1, 10)
		gold.tags |= {IsItem}
	
	return world