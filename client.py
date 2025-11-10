#!/usr/bin/env python3
from __future__ import annotations

import tcod.console
import tcod.context
import tcod.tileset

import g
import game.states
import game.systems

from game.components import MessageLog

import sys

import logging
logger = logging.getLogger("EWClient")

def main(log_level) -> None:
	logging.basicConfig(filename=g.LOG_FILENAME, format=g.LOG_FORMAT, filemode="w", level=log_level)
	logging.info('World client started')

	""" Start the message log """
	g.messages = MessageLog()

	logging.debug(f"Loading tileset {g.GAME_TILESET_FILENAME}")
	tileset = tcod.tileset.load_tilesheet(
		g.GAME_TILESET_FILENAME, columns=16, rows=16, charmap=tcod.tileset.CHARMAP_CP437
	)
	tcod.tileset.procedural_block_elements(tileset=tileset)

	logging.debug(f"Starting main menu state")
	g.states = [game.states.MainMenu()]

	logging.debug(f"Starting main console")
	g.console = tcod.console.Console(g.SCREEN_WIDTH, g.SCREEN_HEIGHT, order="F")

	logging.debug(f"Starting main context")
	with tcod.context.new(
		console=g.console,
		tileset=tileset,
		title=g.GAME_TITLE,
	) as g.context:
		logging.debug('Starting main game loop')
		while g.states:
			game.systems.main_draw()
			game.systems.main_input()

	logging.info('World client stopped')

if __name__ == "__main__":
	log_level = logging.INFO
	try:
		if len(sys.argv) >= 2:
			log_level = logging.DEBUG
		if len(sys.argv) > 2:
			raise SystemError()
	except:
		print(f"Usage: {sys.argv[0]} <log_level>")
		print(f"  <log_level> may be DEBUG")
		sys.exit(1)

	main(log_level)