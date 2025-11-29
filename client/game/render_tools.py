""" Tools to assist in presenting the player information """
from __future__ import annotations
import numpy as np
from tcod.ecs import Entity
import client.g as g
import tcod.console
from client.game.components import Energy, Graphic, Health, IsPlaying, Maps, Position, World, Vision
from client.game.tags import IsActor, IsPlayer, IsWorld
import client.tile_types as tile_types
import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

def player_states(player: Entity, console: tcod.console.Console) -> None:
	health = player.components[Health]
	energy = player.components[Energy]
	x, y = 61, 1
	console.print(x=x, y=y, text=f"Health {health}", fg=(255, 255, 255), bg=(0, 0, 0))
	console.print(x=x, y=y+1, text=f"Energy {energy}", fg=(255, 255, 255), bg=(0, 0, 0))

def world_map(map_idx, console: tcod.console.Console, view_port: tuple) -> None:
#	logger.debug(f"World->render( map_idx {map_idx}, console )")
	(world,) = g.game.Q.all_of(tags=[IsWorld])
	maps = world.components[Maps]

	visible_tiles = maps.maps[map_idx]['visible']
	explored_tiles = maps.maps[map_idx]['explored']
	light_tiles = maps.maps[map_idx]['tiles']['light']
	dark_tiles = maps.maps[map_idx]['tiles']['dark']

	view_x1, view_x2, view_y1, view_y2 = view_port

	console.rgb[0:config.VIEW_PORT_WIDTH, 0:config.VIEW_PORT_HEIGHT] = np.select(
		condlist=[visible_tiles[view_x1:view_x2, view_y1:view_y2], explored_tiles[view_x1:view_x2, view_y1:view_y2]],
		choicelist=[light_tiles[view_x1:view_x2, view_y1:view_y2], dark_tiles[view_x1:view_x2, view_y1:view_y2]],
		default=tile_types.SHROUD
	)

def entities(map_idx: int, console: tcod.console.Console, view_port: tuple) -> None:
	logger.debug(f"World->render( map_idx {map_idx}, console )")
	view_x1, view_x2, view_y1, view_y2 = view_port
	# Render all entities with a position and a face/presentation
	for entity in g.game.Q.all_of(tags=[IsActor],components=[Position, Graphic]):
		pos = entity.components[Position]
		if not (view_x1 <= pos.x < view_x2 and view_y1 <= pos.y < view_y2):
			continue
		graphic = entity.components[Graphic]
		x = pos.x - view_x1, 
		y = pos.y - view_y1,
		console.rgb[["ch", "fg"]][x, y] = graphic.face, graphic.colour

def player(player: Entity, console: tcod.console.Console, view_port: tuple) -> None:
	# Render player entity as the last to ensure it is in front
	view_x1, view_x2, view_y1, view_y2 = view_port
	pos = player.components[Position]
	graphic = player.components[Graphic]
	x = pos.x - view_x1, 
	y = pos.y - view_y1,
	console.rgb[["ch", "fg"]][x, y] = graphic.face, graphic.colour
