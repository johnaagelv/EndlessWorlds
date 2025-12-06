from __future__ import annotations

import attrs
import numpy as np
import tcod.console
import tcod.event
from tcod.event import KeySym, Modifier

import client.g as g
from client.constants import DIRECTION_KEYS, ACTION_KEYS, STAIR_KEYS
from client.game.state import Pop, Push, Reset, State, StateResult
from client.game.components import actor_cid, Maps, Position, Vision
from client.game.tags import IsPlayer, IsWorld
import client.game.world_tools as world_tools
import client.game.entity_tools as entity_tools
import client.game.menus
import client.game.connect_tools
import client.game.render_tools as renders
import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

@attrs.define()
class InGame(State):
	""" Primary in-game state """

	def on_event(self, event: tcod.event.Event) -> StateResult:
		""" Handle events for the in-game state """
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
		match event:
		
			case tcod.event.KeyDown(sym=sym, mod=mod) if (sym, mod) in STAIR_KEYS:
				action = STAIR_KEYS[sym, mod]
				if world_tools.in_gateway(player.components[Position].x, player.components[Position].y, player.components[Position].m):
					gateway = world_tools.go_gateway(player.components[Position].x, player.components[Position].y, player.components[Position].m, action)
					world_tools.start_map(gateway["gateway"]["m"])
					# Move to x, y coordinate in map number m
					player.components[Position] = Position(gateway["gateway"]["x"], gateway["gateway"]["y"], gateway["gateway"]["m"])

			case tcod.event.KeyDown(sym=sym, mod=mod) if (sym, mod) in ACTION_KEYS:
				match (sym, mod):
					case (KeySym.D, Modifier.NONE):
						return Push(Drop())
					case (KeySym.COMMA, Modifier.NONE):
						return Push(Pickup())
				return None

			case tcod.event.KeyDown(sym=sym) if sym in DIRECTION_KEYS:
				player.components[Position] += DIRECTION_KEYS[sym]
				return None

			case tcod.event.KeyDown(sym=KeySym.ESCAPE):
				return Push(MainMenu())

			case tcod.event.Quit():
				return Push(MainMenu())

			case _:
				return None

	def on_draw(self, console: tcod.console.Console) -> None:
		""" Draw the stancard screen """
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
		pos = player.components[Position]

		# Ensure that the FOV is updated
		entity_tools.fov()

		# Get the view port for the rendering methods
		view_port = world_tools.get_view_port(pos)

		# Render the current map
		renders.world_map(pos.m, console, view_port)

		# Draw the entities including the player
		renders.entities(pos.m, console, view_port)
		renders.player(player, console, view_port)

		# Draw the player information
		renders.player_states(player, console)
		
		# Draw any messages
		if text := g.game[None].components.get(("Text", str)):
			console.print(x=0, y=console.height - 1, text=text, fg=(255, 255, 255), bg=(0, 0, 0))

	def on_connect(self) -> None:
		""" Connect to the server for information"""
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
		pos = player.components[Position]
		cid = player.components[actor_cid]
		(world,) = g.game.Q.all_of(tags=[IsWorld])
		maps = world.components[Maps]

		fos_request = {
			"cmd": "fos",
			"cid": cid,
			"x": pos.x,
			"y": pos.y,
			"z": 0,
			"m": pos.m,
			"r": player.components[Vision]
		}
		result = client.game.connect_tools.query_server(fos_request)
		temp = np.array(result['view'])
		maps.maps[pos.m]["tiles"][result["x_min"]:result["x_max"],result["y_min"]:result["y_max"]] = temp
		maps.maps[pos.m]["actors"] = result["actors"]
		world.components[Maps] = Maps(maps.maps, maps.defs)
		return None

class MainMenu(client.game.menus.ListMenu):
	""" Main/escape menu """
	__slots__ = ()

	def __init__(self) -> None:
		""" Initialize the main menu """
		items = [
			client.game.menus.SelectItem("New game", self.new_game, 100),
		]
		if hasattr(g, "world"):
			# We got a world, so add the continue menu item
			items.append(client.game.menus.SelectItem("Continue", self.continue_, 800))

		# Add the quit menu item
		items.append(client.game.menus.SelectItem("Quit", self.quit, 900))

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
	def new_game(id: int) -> StateResult:
		""" Begin a new game """
		g.game = world_tools.new_game()
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
		world_tools.start_map( player.components[Position].m )
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
