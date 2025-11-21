from __future__ import annotations

import attrs
import tcod.console
import tcod.event
from tcod.event import KeySym

import client.g as g

from client.constants import DIRECTION_KEYS
from client.game.state import Pop, Push, Reset, State, StateResult
from client.game.components import Graphic, Position
from client.game.tags import IsPlayer
import client.game.world_tools
import client.game.menus

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
		match event:
			case tcod.event.KeyDown(sym=sym) if sym in DIRECTION_KEYS:
				player.components[Position] += DIRECTION_KEYS[sym]
				return None
			case tcod.event.KeyDown(sym=KeySym.ESCAPE):
				return Push(MainMenu())
			case _:
				return None

	def on_draw(self, console: tcod.console.Console) -> None:
		""" Draw the stancard screen """
		logger.debug('InGame->on_draw( console ) -> None')
		# TODO: Draw the map

		# Draw the entities
		for entity in g.game.Q.all_of(components=[Position, Graphic]):
			pos = entity.components[Position]
			if not (0 <= pos.x < console.width and 0 <= pos.y < console.height):
				continue

			graphic = entity.components[Graphic]
			console.rgb[["ch", "fg"]][pos.y, pos.x] = graphic.face, graphic.colour
		
		# Draw any messages
		if text := g.game[None].components.get(("Text", str)):
			console.print(x=0, y=console.height - 1, text=text, fg=(255, 255, 255), bg=(0, 0, 0))

	def on_connect(self) -> StateResult:
		logger.debug('InGame->on_connect() -> StateResult')
		return None

class MainMenu(client.game.menus.ListMenu):
	""" Main/escape menu """
	__slots__ = ()

	def __init__(self) -> None:
		""" Initialize the main menu """
		logger.debug('MainMenu->__init__() -> None')
		items = [
			client.game.menus.SelectItem("Choose world", self.choose_world, 0),
			client.game.menus.SelectItem("New game", self.new_game, 100),
		]
		if hasattr(g, "world"):
			# Add the continue menu item
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
		logger.debug('MainMenu->continue_( id ) -> None')
		""" Return to the game """
		return Reset(InGame())
	
	@staticmethod
	def new_game(id: int) -> StateResult:
		logger.debug('MainMenu->new_game( id ) -> None')
		""" Begin a new game """
		g.game = client.game.world_tools.new_game()
		return Reset(InGame())

	@staticmethod
	def choose_world(id: int) -> StateResult:
		logger.debug('MainMenu->choose_world( id ) -> StateResult')
		""" Choose a world """
		return Push(WorldMenu())

	@staticmethod
	def quit(id: int) -> StateResult:
		logger.debug('MainMenu->quit( id ) -> StateResult')
		""" Close the program """
		raise SystemExit()

class WorldMenu(client.game.menus.ListMenu):
	""" World menu """
	__slots__ = ('worlds')

	def __init__(self) -> None:
		logger.debug('WorldMenu->__init__() -> None')
		self.worlds = client.game.world_tools.load_worlds()
		items: list = []
		for id, world in enumerate(self.worlds):
			items.append(
				client.game.menus.SelectItem(world["name"], self.load_world, id)
			)
		super().__init__(
			items=tuple(items),
			selected=0,
			x=7,
			y=7,
		)

	def load_world(self, id: int) -> StateResult:
		logger.debug('WorldMenu->load_world( id ) -> StateResult')
		""" Load a world from a world server """
		client.game.world_tools.load_world()
		return Reset(MainMenu())
