from __future__ import annotations

import attrs
import tcod.console
import tcod.event
from tcod.event import KeySym

import client.g as g

from client.constants import DIRECTION_KEYS
from client.game.state import Push, Reset, State, StateResult
from client.game.components import Graphic, Position
from client.game.tags import IsPlayer
import client.game.world_tools
import client.game.menus

@attrs.define()
class InGame(State):
	""" Primary in-game state """

	def on_event(self, event: tcod.event.Event) -> StateResult:
		""" Handle events for the in-game state """
		(player,) = g.world.Q.all_of(tags=[IsPlayer])
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
		# TODO: Draw the map

		# Draw the entities
		for entity in g.world.Q.all_of(components=[Position, Graphic]):
			pos = entity.components[Position]
			if not (0 <= pos.x < console.width and 0 <= pos.y < console.height):
				continue

			graphic = entity.components[Graphic]
			console.rgb[["ch", "fg"]][pos.y, pos.x] = graphic.face, graphic.colour
		
		# Draw any messages
		if text := g.world[None].components.get(("Text", str)):
			console.print(x=0, y=console.height - 1, text=text, fg=(255, 255, 255), bg=(0, 0, 0))

class MainMenu(client.game.menus.ListMenu):
	""" Main/escape menu """
	__slots__ = ()

	def __init__(self) -> None:
		""" Initialize the main menu """
		items = [
			client.game.menus.SelectItem("New game", self.new_game),
			client.game.menus.SelectItem("Quit", self.quit),
		]
		if hasattr(g, "world"):
			items.insert(0, client.game.menus.SelectItem("Continue", self.continue_))

		super().__init__(
			items=tuple(items),
			selected=0,
			x=5,
			y=5,
		)

	@staticmethod
	def continue_() -> StateResult:
		""" Return to the game """
		return Reset(InGame())
	
	@staticmethod
	def new_game() -> StateResult:
		""" Begin a new game """
		g.world = client.game.world_tools.new_world()
		return Reset(InGame())

	@staticmethod
	def quit() -> StateResult:
		""" Close the program """
		raise SystemExit()
