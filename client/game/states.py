""" Derived states used in the game """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

import attrs
import tcod.console
import tcod.event
from tcod.event import KeySym

import g
from game.tags import IsPlayer, IsItem
from game.constants import DIRECTION_KEYS
from game.components import Position, Gold, Graphic
from game.state import Push, Reset, State, StateResult
import game.menus
import game.world_tools


""" Primary in-game state """
@attrs.define()
class InGame(State):

	def on_draw(self, console: tcod.console.Console) -> None:
		logger.info("InGame(State)->on_draw( console ) -> None")
		for entity in g.world.Q.all_of(components=[Position, Graphic]):
			pos = entity.components[Position]
			if not (0 <= pos.x < console.width and 0 <= pos.y < console.height):
				continue
			graphic = entity.components[Graphic]
			console.rgb[["ch", "fg"]][pos.y, pos.x] = graphic.ch, graphic.fg
		
		# If any text added in the world, print it
		if text := g.world[None].components.get(("Text", str)):
			console.print(x=0, y=console.height - 2, text=text, fg=(255, 255, 255), bg=(0, 0, 192))

	""" Handle events for the in-game state """	
	def on_event(self, event: tcod.event.Event) -> StateResult:
		logger.info("InGame(State)->on_event( event ) -> StateResult")
		# Get the player
		(player,) = g.world.Q.all_of(tags=[IsPlayer])
		match event:
			case tcod.event.Quit():
				raise SystemExit
			case tcod.event.KeyDown(sym=sym) if sym in DIRECTION_KEYS:
				player.components[Position] += DIRECTION_KEYS[sym]

				# Auto pickup gold
				for gold in g.world.Q.all_of(components=[Gold], tags=[player.components[Position], IsItem]):
					player.components[Gold] += gold.components[Gold]
					text = f"Got myself some {gold.components[Gold]}g, total: {player.components[Gold]}g"
					# Add the text into the world
					g.world[None].components[("Text", str)] = text
					gold.clear()
				return None
			case tcod.event.KeyDown(sym=KeySym.ESCAPE):
				return Push(MainMenu())
			case _:
				return None

""" Main/escape menu """
class MainMenu(game.menus.ListMenu):
	__slotes__ = ()
	def __init__(self) -> None:
		logger.info("MainMenu(game.menus.ListMenu)->__init__() -> None")
		items = [
			game.menus.SelectItem("New game", self.new_game),
			game.menus.SelectItem("Quit", self.quit),
		]
		if hasattr(g, "world"):
			items.insert(0, game.menus.SelectItem("Continue", self.continue_))
		
		super().__init__(
			items=tuple(items),
			selected=0,
			x=5,
			y=5,
		)
	@staticmethod
	def continue_() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->continue() -> StateResult")
		return Reset(InGame())

	@staticmethod
	def new_game() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->new_game() -> StateResult")
		g.world = game.world_tools.new_world()
		return Reset(InGame())
	
	@staticmethod
	def quit() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->quit() -> StateResult")
		raise SystemExit
