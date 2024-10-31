#!/usr/bin/env python3
import tcod

#import config

from entities import TEntity
from input_handlers import TEventHandler

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50


def main() -> None:
	screen_width = SCREEN_WIDTH
	screen_height = SCREEN_HEIGHT

	tileset = tcod.tileset.load_tilesheet(
		"dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
	)

	player = TEntity(
		x = int(SCREEN_WIDTH / 2),
		y = int(SCREEN_HEIGHT / 2),
		face = "@",
		colour = (255, 255, 255),
	)

	npc = TEntity(
		x = int(SCREEN_WIDTH / 2 - 5),
		y = int(SCREEN_HEIGHT / 2 - 3),
		face = "g",
		colour = (0, 255, 0),
	)

	entities = {npc, player}

	event_handler = TEventHandler()

	with tcod.context.new_terminal(
		screen_width,
		screen_height,
		tileset = tileset,
		title = "Endless Worlds, Ankt",
		vsync = True,
	) as context:
		root_console = tcod.console.Console(screen_width, screen_height, order="F")


		while player.data["game_active"]:

			root_console.print(
				x = player.data["x"],
				y = player.data["y"],
				string = player.data["face"]
			)

			# Present the root console
			context.present(root_console)

			# Clear the root console for updates
			root_console.clear()

			for event in tcod.event.wait():
				action = event_handler.dispatch(event)

				if action is None:
					continue
				
				player.run(action)
				

if __name__ == "__main__":
	main()