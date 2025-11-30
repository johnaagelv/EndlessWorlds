""" Tools to assist in presenting the player information """
from __future__ import annotations
import numpy as np
from tcod.ecs import Entity
import client.g as g
import tcod.console
from client.game.components import Graphic, Maps, Position, state_name, state_value, state_max
from client.game.tags import IsActor, IsState, IsWorld
import client.tile_types as tile_types
import client.ui.colours as colours
import client.ui.configuration as config

def player_states(player: Entity, console: tcod.console.Console) -> None:
	""" Render all the player states such as health, energy, ... """
	view_x = config.STATE_PORT_X
	view_y = config.STATE_PORT_Y
	view_width = config.STATE_PORT_WIDTH
	for player_state in g.game.Q.all_of(tags=[IsState]):
		current_value = int(player_state.components[state_value] / 1000)
		max_value = int(player_state.components[state_max] / 1000)
		bar_width = int(float(player_state.components[state_value]) / player_state.components[state_max] * view_width)
		bar_level = float(current_value / max_value)
		bar_filled = colours.bar_low
		if bar_level > 0.3:
			bar_filled = colours.bar_high
		elif bar_level > 0.2:
			bar_filled = colours.bar_medium
		
		console.draw_rect(
			x = view_x,
			y = view_y,
			width = view_width,
			height = 1,
			ch = 1,
			bg = colours.bar_empty
		)
		if bar_width > 0:
			console.draw_rect(
				x = view_x,
				y = view_y,
				width = bar_width,
				height = 1,
				ch = 1,
				bg = bar_filled
			)
		console.print(view_x, view_y, text=f"{player_state.components[state_name]}", fg=colours.bar_text)
		state_x = view_width - 2 - (current_value > 9) - (current_value > 99) - (current_value > 999)
		console.print(view_x + state_x, view_y, text=f"{current_value}", fg=colours.bar_text)
		view_y += 1

def world_map(map_idx, console: tcod.console.Console, view_port: tuple) -> None:
	""" Render the world map in the view port and render the name of the map """
	(world,) = g.game.Q.all_of(tags=[IsWorld])
	maps = world.components[Maps]

	visible_tiles = maps.maps[map_idx]['visible']
	explored_tiles = maps.maps[map_idx]['explored']
	light_tiles = maps.maps[map_idx]['tiles']['light']
	dark_tiles = maps.maps[map_idx]['tiles']['dark']

	# Transfer the tiles within the view port to the console
	view_x1, view_x2, view_y1, view_y2 = view_port
	console.rgb[0:config.VIEW_PORT_WIDTH, 0:config.VIEW_PORT_HEIGHT] = np.select(
		condlist=[visible_tiles[view_x1:view_x2, view_y1:view_y2], explored_tiles[view_x1:view_x2, view_y1:view_y2]],
		choicelist=[light_tiles[view_x1:view_x2, view_y1:view_y2], dark_tiles[view_x1:view_x2, view_y1:view_y2]],
		default=tile_types.SHROUD
	)
	console.print(x=config.WORLD_PORT_X, y=config.WORLD_PORT_Y, text=f"{maps.maps[map_idx]['name']}", fg=colours.bar_text)


def entities(map_idx: int, console: tcod.console.Console, view_port: tuple) -> None:
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
