#!/usr/bin/env python3
from __future__ import annotations

import tcod.console
import tcod.context
import tcod.tileset
from tcod.ecs import Registry

import client.g as g
import client.game.states
import client.game.world_tools
import client.game.state_tools

import client.configuration as config
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

	# Activate the global console
	g.console = tcod.console.Console(config.CONSOLE_WIDTH, config.CONSOLE_HEIGHT)
	# Initialize the registry
	g.game = Registry()
	# Activate the global state stack
	g.states = [client.game.states.MainMenu()]

	# RUN
	with tcod.context.new(
		console=g.console,
		tileset=tileset,
	) as g.context:
		client.game.state_tools.main_loop()

	logger.info(f"{config.APP_TITLE} stopped")

if __name__ == "__main__":
	log_level = config.LOG_LEVEL_CLIENT
	log_level = logging.DEBUG
	# TODO: Use argparser here for log_level as parameter (see the server.py)
	main(log_level)