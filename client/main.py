#!/usr/bin/env python3
import tcod

from renders import TRender
from entities import TActor
from worlds import TWorld
from input_handlers import TEventHandler

from libclient import TClient, TMessage

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
	
def main() -> None:
	player_template = {
		"x": 2, # X coordinate in map m
		"y": 2, # Y coordinate in map m
		"m": 0, # Map number
		"face": "@", # How I look like
		"colour": (255, 255, 255),
		"playing": True, # Am I playing or not
		"world": TWorld,
	}

	player = TActor(data=player_template)

	event_handler = TEventHandler()

	player.data["world"] = TWorld()

	# Establish a render for presenting the game UI
	render = TRender(config)

	# Start the communicator
	client = TClient()

	# Run the game loop
	while player.is_playing == True:
		# Render the player view to console
		render.render_world(player.map)
		render.render_actor(player.me)
		render.render()

		# Get user input
		for event in tcod.event.wait(timeout=5):
			action = event_handler.dispatch(event)

			if action is None:
				continue
		
			action.run(player)

if __name__ == "__main__":
	main()