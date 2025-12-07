""" Tools assisting the entity capabilities """
from __future__ import annotations

from tcod.ecs import Entity
import community.g as g
from tcod.map import compute_fov
from community.game.components import Maps, Position, Vision
from community.game.tags import IsWorld

import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

def fov(actor: Entity) -> None:
	
	(world,) = g.game.Q.all_of(tags=[IsWorld])
	pos = actor.components[Position]
	vision = actor.components[Vision]
	maps = world.components[Maps]

	maps.maps[pos.m]['visible'][:] = compute_fov(
		maps.maps[pos.m]['tiles']['transparent'],
		(pos.x, pos.y),
		radius = vision
	)
	maps.maps[pos.m]['explored'] |= maps.maps[pos.m]['visible']
