#!/usr/bin/env python3
import sys
import tcod
import numpy as np

from renders import TRender
from entities import TActor
from worlds import TWorld
from input_handlers import TEventHandler
from clients import TClient

import logging
logger = logging.getLogger("EWClient")
LOG_FILENAME = "EWclient.log"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

config = {
	"title": "Endless Worlds, Ankt, (c) 2025",
	"screen_width": SCREEN_WIDTH,
	"screen_height": SCREEN_HEIGHT,
	"tileset": "client/dejavu10x10_gs_tc.png",
	"host": "192.168.1.104",
	"port": 12345,
}
	
def main(log_level) -> None:
	logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT, filemode="w", level=log_level)
	logging.info('World client started')

	player_template = {
		"x": 2, # X coordinate in map m
		"y": 2, # Y coordinate in map m
		"z": 0, # Z coordinate in map m
		"r": 4, # Vision sense radius
		"m": -1, # Map number
		"face": "@", # How I look like
		"colour": (255, 255, 255),
		"playing": True, # Am I playing or not
		"world": None,
	}

	player = TActor(data=player_template)

	event_handler = TEventHandler(player)
	# Establish a render for presenting the game UI
	render = TRender(config)
	client = TClient()

	while player.is_playing == True:
		# Render the player view to console
		if player.data['world'] is not None:
			render.render_world(player)
			render.render_actor(player)
			render.render()

			# Get user input
			for event in tcod.event.wait(timeout=5):
				action = event_handler.dispatch(event)

				if action is None:
					continue
			
				action.run()

		# Ready the communicator
		request = player.run()

		if request is not None:
			client.start_connection(config["host"], config["port"], request)
			
			while client.run(player):
				pass

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