from __future__ import annotations

import attrs
import tcod.console
import tcod.event
from tcod.event import KeySym, Modifier

import client.g as g

from client.constants import DIRECTION_KEYS, ACTION_KEYS, STAIR_KEYS
from client.game.state import Pop, Push, Reset, State, StateResult
from client.game.components import Graphic, Position, Vision, World
from client.game.tags import IsPlayer, IsWorld
import client.game.world_tools
import client.game.menus
import client.game.connect_tools
import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

@attrs.define()
class InGame(State):
	""" Primary in-game state """

	def on_event(self, event: tcod.event.Event) -> StateResult:
		""" Handle events for the in-game state """
		logger.debug('InGame->on_event( event ) -> StateResult')
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
		(world,) = g.game.Q.all_of(tags=[IsWorld])
#		map = world.components[World].maps[player.components[Position].m]
		match event:
			case tcod.event.KeyDown(sym=sym) if sym in DIRECTION_KEYS:
				player.components[Position] += DIRECTION_KEYS[sym]
				return None
			
			case tcod.event.KeyDown(sym=sym, mod=mod) if (sym, mod) in STAIR_KEYS:
				action = STAIR_KEYS[sym, mod]
				match action:
					case "up":
						print(f"up: {world.components[World].in_gateway(player.components[Position].x, player.components[Position].y, player.components[Position].m)}")
						if world.components[World].in_gateway(player.components[Position].x, player.components[Position].y, player.components[Position].m):
							gateway = world.components[World].go_gateway(player.components[Position].x, player.components[Position].y, player.components[Position].m, "up")
							# Move to x, y coordinate in map number m
							player.components[Position] = Position(gateway["gateway"]["x"], gateway["gateway"]["y"], gateway["gateway"]["m"])
					case "down":
						if world.components[World].in_gateway(player.components[Position].x, player.components[Position].y, player.components[Position].m):
							gateway = world.components[World].go_gateway(player.components[Position].x, player.components[Position].y, player.components[Position].m, "down")
							# Move to x, y coordinate in map number m
							player.components[Position] = Position(gateway["gateway"]["x"], gateway["gateway"]["y"], gateway["gateway"]["m"])

			case tcod.event.KeyDown(sym=sym, mod=mod) if (sym, mod) in ACTION_KEYS:
				match (sym, mod):
					case (KeySym.D, Modifier.NONE):
						return Push(Drop())
					case (KeySym.COMMA, Modifier.NONE):
						return Push(Pickup())
				return None

			case tcod.event.KeyDown(sym=KeySym.ESCAPE):
				return Push(MainMenu())

			case tcod.event.Quit():
				return Push(MainMenu())

			case _:
				return None

	def on_draw(self, console: tcod.console.Console) -> None:
		""" Draw the stancard screen """
		logger.debug('InGame->on_draw( console ) -> None')
		# Draw the world
		(world,) = g.game.Q.all_of(tags=[IsWorld])
		(player,) = g.game.Q.all_of(tags=[IsPlayer])

		map_idx = player.components[Position].m

		view_width = config.VIEW_PORT_WIDTH
		view_height = config.VIEW_PORT_HEIGHT

		width = world.components[World].maps[map_idx]["width"]
		height = world.components[World].maps[map_idx]["height"]

		view_x1 = min(max(0, player.components[Position].x - int(view_width / 2)), width - view_width)
		view_x2 = view_x1 + view_width

		view_y1 = min(max(0, player.components[Position].y - int(view_height / 2)), height - view_height)
		view_y2 = view_y1 + view_height

		# Render the current map
		world.components[World].render(map_idx, console, (view_x1, view_x2, view_y1, view_y2))

		# Draw the entities
		for entity in g.game.Q.all_of(components=[Position, Graphic]):
			pos = entity.components[Position]
			if not (view_x1 <= pos.x < view_x2 and view_y1 <= pos.y < view_y2):
				continue
			graphic = entity.components[Graphic]
			x = pos.x - view_x1, 
			y = pos.y - view_y1,
			console.rgb[["ch", "fg"]][x, y] = graphic.face, graphic.colour
		
		# Draw any messages
		if text := g.game[None].components.get(("Text", str)):
			console.print(x=0, y=console.height - 1, text=text, fg=(255, 255, 255), bg=(0, 0, 0))

	def on_connect(self) -> None:
		""" Connect to the server for information"""
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
#		(world,) = g.game.Q.all_of(tags=[IsWorld])

		fos_request = {
			"cmd": "fos", "cid": "1234",
			"x": player.components[Position].x,
			"y": player.components[Position].y,
			"z": 0,
			"m": player.components[Position].m,
			"r": player.components[Vision]
		}
		result = client.game.connect_tools.query_server(fos_request)
		logger.debug(result)
#		world.components[World].maps[player.components[Map]] = result["view"]
		return None

class MainMenu(client.game.menus.ListMenu):
	""" Main/escape menu """
	__slots__ = ()

	def __init__(self) -> None:
		""" Initialize the main menu """
		logger.debug('MainMenu->__init__() -> None')
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
		logger.debug('MainMenu->continue_( id ) -> None')
		return Reset(InGame())
	
	@staticmethod
	def new_game(id: int) -> StateResult:
		""" Begin a new game """
		logger.debug('MainMenu->new_game( id ) -> None')
		g.game = client.game.world_tools.new_game()
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
		(world,) = g.game.Q.all_of(tags=[IsWorld])
		world.components[World].start_map( player.components[Position].m)
		return Reset(InGame())

	@staticmethod
	def quit(id: int) -> StateResult:
		""" Close the program """
		logger.debug('MainMenu->quit( id ) -> StateResult')
		raise SystemExit

@attrs.define()
class Pickup(State):
	def on_event(self, event: tcod.event.Event) -> StateResult:
		""" Handle events for picking up items from player location """
		logger.debug('Pickup->on_event( event ) -> StateResult')
		return Pop()
	
	def on_draw(self, console: tcod.console.Console) -> None:
		""" Present the items on player location available for pickup """
		return None

@attrs.define()
class Drop(State):
	def on_event(self, event: tcod.event.Event) -> StateResult:
		""" Handle events for dropping items from the inventory """
		logger.debug("Drop->on_event( event ) -> StateResult")
		return Pop()
	
	def on_draw(self, console: tcod.console.Console) -> None:
		""" Present the inventory for item drop """
		return None
