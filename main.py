#!/usr/bin/env python3
import copy
import traceback

import tcod

import colours as colour
from engine import TEngine
import entity_factories
from procgen import generate_dungeon

def main() -> None:
	screen_width = 80
	screen_height = 50

	map_width = 80
	map_height = 43

	tileset = tcod.tileset.load_tilesheet(
		"dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
	)

	player = copy.deepcopy(entity_factories.player)

	engine = TEngine(player=player)

	engine.game_map = generate_dungeon(
		map_width=map_width,
		map_height=map_height,
		engine=engine,
	)
	engine.update_fov()
	
	engine.message_log.add_message("Hello and welcome, Adventurer, to Endless Worlds!", colour.welcome_text)

	with tcod.context.new_terminal(
		screen_width,
		screen_height,
		tileset=tileset,
		title="Yet Another Roguelike Tutorial",
		vsync=True,
	) as context:
		root_console = tcod.console.Console(screen_width, screen_height, order="F")
		while True:
			root_console.clear()
			engine.event_handler.on_render(console=root_console)
			context.present(root_console)
			try:
				for event in tcod.event.wait(timeout=2.0):
					context.convert_event(event)
					engine.event_handler.handle_events(event)
			except Exception:
				traceback.print_exc()
				engine.message_log.add_message(traceback.format_exc(), colour.error)

if __name__ == "__main__":
	main()
