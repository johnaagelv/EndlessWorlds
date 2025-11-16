#!/usr/bin/env python3
from __future__ import annotations

import configuration as config

import tcod.console
import tcod.context
import tcod.tileset

from client.states import ExampleState

import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

def main(log_level: int) -> None:
	logging.basicConfig(filename=config.LOG_FILENAME_CLIENT, format=config.LOG_FORMAT, filemode="w", level=log_level)
	logger.info(f"{config.APP_TITLE} started")

	# Load the tileset to use for console presentation
	tileset = tcod.tileset.load_tilesheet(
		config.GAME_TILESET_FILENAME, columns=16, rows=16, charmap=tcod.tileset.CHARMAP_CP437
	)
	tcod.tileset.procedural_block_elements(tileset=tileset)

	console = tcod.console.Console(config.CONSOLE_WIDTH, config.CONSOLE_HEIGHT)

	player = ExampleState(x=console.width // 2, y=console.height // 2)

	with tcod.context.new(
		console=console,
		tileset=tileset,
	) as context:
		while player.is_alive:
			console.clear()
			player.on_draw(console)
			context.present(console)
			for event in tcod.event.wait():
				player.on_event(event)

	logger.info(f"{config.APP_TITLE} stopped")

if __name__ == "__main__":
	log_level = config.LOG_LEVEL_CLIENT
	# TODO: Use argparser here for log_level as parameter (see the server.py)
	main(log_level)