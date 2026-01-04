""" Tools assisting the entity capabilities """
from __future__ import annotations

#import numpy as np
from tcod.constants import FOV_DIAMOND #, FOV_BASIC
from tcod.map import compute_fov
from client.game.components import Position
#from tcod.ecs import Entity

#import client.configuration as config
#import logging
#logger = logging.getLogger(config.LOG_NAME_CLIENT)

def fov(pos: Position, vision: int, map: dict, current_map: bool = True) -> dict:
	"""
	FOV needs map data: visible, tiles[transparent], explored
	Player position and vision
	"""
	map['visible'][:] = compute_fov(
		map['tiles']['transparent'],
		(pos.x, pos.y),
		radius = vision,
		algorithm=FOV_DIAMOND
	)
	map['explored'] |= map['visible']

	return map