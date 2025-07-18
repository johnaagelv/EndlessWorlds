#!/usr/bin/env python3
from __future__ import annotations

import tcod.console
import tcod.context
import tcod.event
import tcod.tileset

import g
import game.states
#import game.world_tools
import game.state_tools

import sys

import logging
logger = logging.getLogger("EWClient")
LOG_FILENAME = "EWclient.log"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
VIEWPORT_WIDTH = SCREEN_WIDTH - 20
VIEWPORT_HEIGHT = SCREEN_HEIGHT - 10
	
def main(log_level) -> None:
	logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT, filemode="w", level=log_level)
	logging.info('World client started')

	tileset = tcod.tileset.load_tilesheet(
		"Alloy_curses_12x12.png", columns=16, rows=16, charmap=tcod.tileset.CHARMAP_CP437
	)
	tcod.tileset.procedural_block_elements(tileset=tileset)

	g.states = [game.states.MainMenu()]
	g.console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
	g.console.print(0, 0, "Endless Worlds, 2025")

	with tcod.context.new(
		console=g.console,
		tileset=tileset,
		title="Endless Worlds, 2025",
	) as g.context:
		game.state_tools.main_loop()

	logging.info('World client stopped')

if __name__ == "__main__":
	log_level = logging.DEBUG
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