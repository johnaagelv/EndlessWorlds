#!/usr/bin/env python3
import tcod
import json

from typing import Dict

from engines import TEngine
from entities import TEntity
from game_map import TGameMap
from connectors import TConnector
from input_handlers import TEventHandler

SERVER_HOST = "192.168.1.104"
SERVER_PORT = 65432

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 45

def load_data() -> Dict:
	with open("save.sav", "rt") as f:
		data = json.load(f)
	return data

def main() -> None:
	screen_width = SCREEN_WIDTH
	screen_height = SCREEN_HEIGHT

	map_width = MAP_WIDTH
	map_height = MAP_HEIGHT

	tileset = tcod.tileset.load_tilesheet(
		"dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
	)

	client = TConnector(host=SERVER_HOST, port=SERVER_PORT)

	player = TEntity(client=client)

	data = load_data()
	player.load(data=data)

	event_handler = TEventHandler()

	game_map = TGameMap(map_width, map_height)

	engine = TEngine(player=player, event_handler=event_handler, game_map=game_map)

	with tcod.context.new_terminal(
		screen_width,
		screen_height,
		tileset = tileset,
		title = "Endless Worlds, Ankt",
		vsync = True,
	) as context:
		root_console = tcod.console.Console(screen_width, screen_height, order="F")
		while player.data["playing"]:
			engine.render(root_console, context)
			events = tcod.event.wait(timeout=5.0)
			print("Waiting finished")
			engine.handle_events(events)
			

if __name__ == "__main__":
	main()