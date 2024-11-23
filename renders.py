from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

import colours as colour

if TYPE_CHECKING:
	from tcod import console
	from engine import TEngine
	from game_map import TGameMap

def get_names_at_location(x: int, y: int, game_map: TGameMap) -> str:
	if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
		return ""
	
	names = ", ".join(entity.name for entity in game_map.entities if entity.x == x and entity.y == y)
	return names.capitalize()

def render_bar(console: console.Console, current_value: int, maximum_value: int, total_width: int) -> None:
	bar_width = int(float(current_value) / maximum_value * total_width)

	console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=colour.bar_empty)

	if bar_width > 0:
		console.draw_rect(x=0, y=45, width=bar_width, height=1, ch=1, bg=colour.bar_filled)
	
	console.print(x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=colour.bar_text)

def render_dungeon_level(console: console.Console, dungeon_level: int, location: Tuple[int, int]) -> None:
	x, y = location
	console.print(x=x, y=y, string=f"Level: {dungeon_level}")

def render_names_at_mouse_location(console: console.Console, x: int, y: int, engine: TEngine) -> None:
	mouse_x, mouse_y = engine.mouse_location
	names_at_mouse_location = get_names_at_location(x=mouse_x, y=mouse_y, game_map=engine.game_map)
	console.print(x=x, y=y, string=names_at_mouse_location)

def render_stairs(console: console.Console, location: Tuple[int, int], engine: TEngine) -> None:
	x, y = location
	stair_locations = f"D({engine.game_map.downstairs_location[0]},{engine.game_map.downstairs_location[1]}), U({engine.game_map.upstairs_location[0]},{engine.game_map.upstairs_location[1]})"
	console.print(x=x, y=y, string=stair_locations)