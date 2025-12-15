""" Tools assisting the entity capabilities """
from __future__ import annotations

import client.g as g
from tcod.constants import FOV_DIAMOND #, FOV_BASIC
from tcod.map import compute_fov
from client.game.components import Maps, Position, Vision
from client.game.tags import IsPlayer, IsWorld

import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

def fov() -> None:
	(player,) = g.game.Q.all_of(tags=[IsPlayer])
	(world,) = g.game.Q.all_of(tags=[IsWorld])
	pos = player.components[Position]
	vision = player.components[Vision]
	maps = world.components[Maps]

	maps.maps[pos.m]['visible'][:] = compute_fov(
		maps.maps[pos.m]['tiles']['transparent'],
		(pos.x, pos.y),
		radius = vision,
		algorithm=FOV_DIAMOND
	)
	maps.maps[pos.m]['explored'] |= maps.maps[pos.m]['visible']
