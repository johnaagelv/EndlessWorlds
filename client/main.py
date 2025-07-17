#!/usr/bin/env python3
from __future__ import annotations
import sys
import tcod

from renders import TRender
from entities import TActor
from input_handlers import TEventHandler
from clients import TClient
from message_logs import TMessageLog

import logging
logger = logging.getLogger("EWClient")
LOG_FILENAME = "EWclient.log"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
VIEWPORT_WIDTH = SCREEN_WIDTH - 20
VIEWPORT_HEIGHT = SCREEN_HEIGHT - 10

config = {
	"title": "Endless Worlds, 2025",
	"layout": "sc8050vp6040sp2005lp6005",
	"layouts": {
		"sc8050vp6040sp2005lp6005": {
			"screen_width": 80,
			"screen_height": 50,
			"viewport_x": 0,
			"viewport_y": 0,
			"viewport_width": 60,
			"viewport_height": 40,
			"state_x": 60,
			"state_y": 2,
			"state_width": 20,
			"state_height": 5,
			"log_x": 21,
			"log_y": 41,
			"log_width": 59,
			"log_height": 5,
			"tileset": "redjack17.png",
		},
	},
	"screen_width": SCREEN_WIDTH,
	"screen_height": SCREEN_HEIGHT,
	"viewport_width": VIEWPORT_WIDTH,
	"viewport_height": VIEWPORT_HEIGHT,
	"tileset": "redjack17.png",
	"host": "192.168.1.104",
	"port": 12345,
}
	
def main(log_level) -> None:
	logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT, filemode="w", level=log_level)
	logging.info('World client started')

	message_log = TMessageLog()

	player_template = {
		"x": -1, # X coordinate in map m
		"y": -1, # Y coordinate in map m
		"z": -1, # Z coordinate in map m
		"m": -1, # Map number
		"h": f"{config['host']}:{config['port']}", # Host (address and port)
		"face": "@", # How I look like
		"colour": (255, 255, 255),
		"states": {
			"health": [500000, 0, 1000000], # current, min, max
			"energy": [150000, 0, 1000000],
			"strength": [50000, 0, 1000000],
		},
		"capabilities": {
			"vision": [4], # default vision range
			"hearing": [4],
		},
		"inventory": [],
		"slots": {
			"head": None, # cap, helmet
			"neck": None, # necklace
			"arms": None, # armor
			"left arm": None, # armor, leather arm wraps
			"right arm": None, # armor
			"left wrist": None, # bracelet
			"right wrist": None, # bracelet
			"hands": None, # gloves
			"left hand": None, # weapon, shield
			"right hand": None, # weapon, shield
			"left hand fingers": [None, None, None, None], # rings
			"right hand fingers": [None, None, None, None], # rings
			"body": None, # armor, leather vest
			"waist": None, # tool or weapons belt
			"legs": None, # armor
			"feet": None, # boots
		},
		"playing": True, # Am I playing or not
		"world": None,
	}

	player = TActor(data=player_template)
	player.log = message_log

	event_handler = TEventHandler(player)
	# Establish a render for presenting the game UI
	render = TRender(config['layouts'][config['layout']])
	client = TClient()

	while player.is_playing == True:
		# Render the player view to console
		if player.data['world'] is not None:
			render.render_world(player)
			render.render_actor(player)
			render.render_entities(player)
			render.render_states(player)
			render.render_log(message_log.messages)
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
			client.start_connection(request)
			
			while client.run(player):
				pass

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