""" Tools assisting the entity capabilities """
from __future__ import annotations

#import numpy as np
from tcod.constants import FOV_DIAMOND #, FOV_BASIC
from tcod.map import compute_fov
from client.game.components import Position
#from tcod.ecs import Entity

import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

def fov(pos: Position, vision: int, map: dict, current_map: bool = True) -> None:
	"""
	FOV needs map data: visible, tiles[transparent], explored
	Player position and vision
	"""
#	if pos.x < -vision or pos.x >= map["width"] + vision or pos.y < -vision or pos.y >= map["height"] + vision:
#		return
	x = pos.x
	y = pos.y
	print(f"orig: {pos.m} {x},{y} {map['width']},{map['height']}")
	if current_map:
		pass
	else:
		if x >= 0 and  x < vision:
			x = x + map["width"]
		elif x < map["width"] and x >= map["width"] - vision:
			x = x - map["width"]
		if y >= 0 and y < vision:
			y = y + map["height"]
		elif y < map["height"] and y >= map["height"] - vision:
			y = y - map["height"]
	
	if x < -vision or x >= map["width"] + vision or y < -vision or y >= map["height"] + vision:
		return
	print(f"final: {pos.m} {x},{y} {map['width']},{map['height']}")
	
	map['visible'][:] = compute_fov(
		map['tiles']['transparent'],
		(x, y),
		radius = vision,
		algorithm=FOV_DIAMOND
	)
	map['explored'] |= map['visible']
