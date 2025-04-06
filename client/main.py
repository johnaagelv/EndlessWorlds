#!/usr/bin/env python3
import tcod
import threading
import time
import numpy as np

from renders import TRender
from entities import TActor
from worlds import TWorld
from input_handlers import TEventHandler
import tile_types
from clients import TClient

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

def keyboard_input(player: TActor):
	event_handler = TEventHandler()
	# Establish a render for presenting the game UI
	render = TRender(config)

	while player.is_playing == True:
		# Render the player view to console
#		render.render_world(player.data["world"].maps[player.data["m"]])
		render.render_world(player)
		render.render_actor(player)
		render.render()

		# Get user input
		for event in tcod.event.wait(timeout=5):
			action = event_handler.dispatch(event)

			if action is None:
				continue
		
			action.run(player)

	
def main() -> None:
	player_template = {
		"x": 2, # X coordinate in map m
		"y": 2, # Y coordinate in map m
		"z": 0, # Z coordinate in map m
		"r": 4, # Vision sense radius
		"m": -1, # Map number
		"face": "@", # How I look like
		"colour": (255, 255, 255),
		"playing": True, # Am I playing or not
		"world": TWorld,
	}

	player = TActor(data=player_template)

	player.data["world"] = TWorld()

	keyboard_thread = threading.Thread(target=keyboard_input, args=[player])
	keyboard_thread.daemon = True # Allows program to exit if main thread exits.
	keyboard_thread.start()

	# Ready the communicator
	client = TClient()

	# Run the game loop
	while player.is_playing == True:
		request = player.run()

		if request is not None:
			client.start_connection(config["host"], config["port"], request)
			
			while client.run(player):
				pass

			if player.fos is not None:
				cmd = player.fos
				action = cmd.get("cmd")
				if action == "fos":
					fos = cmd.get("fos")
					x_min = fos.get("x_min")
					x_max = fos.get("x_max")
					y_min = fos.get("y_min")
					y_max = fos.get("y_max")
					view = fos.get("view")
					gateways = fos.get("gateways")
					temp = np.array(view)

					player.data["world"].maps[player.data["m"]]["tiles"][x_min:x_max, y_min:y_max] = temp
					player.data["world"].maps[player.data["m"]]["gateways"] = gateways

				player.fos = None

if __name__ == "__main__":
	main()