from __future__ import annotations

from random import randint
import attrs
import numpy as np
import tcod.console
import tcod.event

import community.g as g
from community.game.state import Pop, Reset, State, StateResult
from community.game.components import CID, Maps, Position, Vision
from community.game.tags import IsPlayer, IsWorld
import community.game.world_tools as world_tools
import community.game.menus
import community.game.connect_tools

#import community.configuration as config
#import logging
#logger = logging.getLogger(config.LOG_NAME_CLIENT)

@attrs.define()
class InGame(State):
	""" Primary in-game state """

	def on_event(self, event: tcod.event.Event) -> StateResult:
		""" Handle events for the in-game state """
		for actor in g.game.Q.all_of(tags=[IsPlayer]):
			pos = actor.components[Position]

			direction = (randint(-1, 1), randint(-1,1))
			if direction != (0, 0):
				actor.components[Position] += direction
			else:
				if world_tools.in_gateway(pos.x, pos.y, pos.m):
					gateway = world_tools.go_gateway(pos.x, pos.y, pos.m)
					world_tools.start_map(gateway["gateway"]["m"])
					# Move to x, y coordinate in map number m
					actor.components[Position] = Position(gateway["gateway"]["x"], gateway["gateway"]["y"], gateway["gateway"]["m"])

	def on_draw(self, console: tcod.console.Console) -> None:
		""" Draw the stancard screen """

	def on_connect(self) -> None:
		""" Connect to the server for information"""
		(world,) = g.game.Q.all_of(tags=[IsWorld])
		maps = world.components[Maps]
		for player in g.game.Q.all_of(tags=[IsPlayer]):
			pos = player.components[Position]
			cid = player.components[CID]

			fos_request = {
				"cmd": "fos",
				"cid": cid,
				"x": pos.x,
				"y": pos.y,
				"m": pos.m,
				"r": player.components[Vision],
#				"face": player.components[Graphic].face
			}
			result = community.game.connect_tools.query_server(fos_request)
			temp = np.array(result['view'])
			maps.maps[pos.m]["tiles"][result["x_min"]:result["x_max"],result["y_min"]:result["y_max"]] = temp
			maps.maps[pos.m]["actors"] = result["actors"]
			world.components[Maps] = Maps(maps.maps, maps.defs)
		return None

class MainMenu(community.game.menus.ListMenu):
	""" Main/escape menu """
	__slots__ = ()

	def __init__(self) -> None:
		""" Initialize the main menu """
		items = [
			community.game.menus.SelectItem("Start village 10", self.village, 10),
			community.game.menus.SelectItem("Start village 50", self.village, 50),
			community.game.menus.SelectItem("Start village 100", self.village, 100),
			community.game.menus.SelectItem("Start village 500", self.village, 500),
		]
		if hasattr(g, "world"):
			# We got a world, so add the continue menu item
			items.append(community.game.menus.SelectItem("Continue", self.continue_, 800))

		# Add the quit menu item
		items.append(community.game.menus.SelectItem("Quit", self.quit, 900))

		super().__init__(
			items=tuple(items),
			selected=0,
			x=5,
			y=5,
		)

	@staticmethod
	def continue_(id: int) -> StateResult:
		""" Return to the game """
		return Reset(InGame())
	
	@staticmethod
	def village(id: int) -> StateResult:
		print(f"Village {id}")
		""" Begin a new game """
		# id = number of actors
		g.game = world_tools.new_game(id)
		for actor in g.game.Q.all_of(tags=[IsPlayer]):
			world_tools.start_map( actor.components[Position].m )
		return Reset(InGame())

	@staticmethod
	def quit(id: int) -> StateResult:
		""" Close the program """
		raise SystemExit

@attrs.define()
class Pickup(State):
	def on_event(self, event: tcod.event.Event) -> StateResult:
		""" Handle events for picking up items from player location """
		return Pop()
	
	def on_draw(self, console: tcod.console.Console) -> None:
		""" Present the items on player location available for pickup """
		return None

@attrs.define()
class Drop(State):
	def on_event(self, event: tcod.event.Event) -> StateResult:
		""" Handle events for dropping items from the inventory """
		return Pop()
	
	def on_draw(self, console: tcod.console.Console) -> None:
		""" Present the inventory for item drop """
		return None
