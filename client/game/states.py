""" Derived states used in the game """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

import os.path
import pickle
import attrs
import tcod.console
import tcod.event
from tcod.event import KeySym

import g
from game.tags import IsPlayer, IsItem, IsActor
from game.constants import DIRECTION_KEYS
from game.components import Gold, Graphic, ExplorationMemory, Position, Visible, Explored
from game.state import Push, Reset, State, StateResult
import game.menus
import game.world_tools
import tcod.ecs

import numpy as np
import tile_types

""" Primary in-game state """
@attrs.define()
class InGame(State):

	def on_draw(self, console: tcod.console.Console) -> None:
		logger.info("InGame(State)->on_draw( console ) -> None")
		# Draw the map
		map: np.ndarray
		visible: np.ndarray
		explored: np.ndarray
		for entity in g.world.Q.all_of(components=[ExplorationMemory]):
			map = entity.components[ExplorationMemory].map
			visible = entity.components[ExplorationMemory].visible
			explored = entity.components[ExplorationMemory].explored

		console.rgb[0:80,0:50] = np.select(
			condlist=[visible, explored],
			choicelist=[map['light'], map['dark']],
			default=tile_types.SHROUD
		)

		# Draw all the items
		for entity in g.world.Q.all_of(components=[Position, Graphic], tags=[IsItem]):
			pos = entity.components[Position]
			if not (0 <= pos.x < console.width and 0 <= pos.y < console.height):
				continue
			graphic = entity.components[Graphic]
			console.rgb[["ch", "fg"]][pos.x, pos.y] = graphic.ch, graphic.fg

		# Draw all the actors, including the player
		for entity in g.world.Q.all_of(components=[Position, Graphic], tags=[IsActor]):
			pos = entity.components[Position]
			if not (0 <= pos.x < console.width and 0 <= pos.y < console.height):
				continue
			graphic = entity.components[Graphic]
			console.rgb[["ch", "fg"]][pos.x, pos.y] = graphic.ch, graphic.fg

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

			case tcod.event.KeyDown(sym=sym) if sym == tcod.event.KeySym.COMMA:
				# Manually pick up the item
				items = g.world.Q.all_of(tags=[player.components[Position], IsItem]).get_entities()
				if len(items) > 1:
					print(f"Pickup of {len(items)} items!")
				for gold in items:
					player.components[Gold] += gold.components[Gold]
#				for gold in g.world.Q.all_of(components=[Gold], tags=[player.components[Position], IsItem]):
#					player.components[Gold] += gold.components[Gold]
					gold.clear()
				return None
			case tcod.event.KeyDown(sym=KeySym.ESCAPE):
				return Push(MainMenu())
			case _:
				return None

""" Main/escape menu """
class MainMenu(game.menus.ListMenu):
	__slots__ = ()
	def __init__(self) -> None:
		logger.info("MainMenu(game.menus.ListMenu)->__init__() -> None")
		items = [
			game.menus.SelectItem("New game", self.new_game),
			game.menus.SelectItem("Quit", self.quit),
		]
		# Check that a savefile exists
		if os.path.exists('savefile.sav'):
			items.insert(1, game.menus.SelectItem("Load game", self.load_))

		if hasattr(g, "world"):
			items.insert(1, game.menus.SelectItem("Continue", self.continue_))
			items.insert(2, game.menus.SelectItem("Save", self.save_))
		
		super().__init__(
			items=tuple(items),
			selected=0,
			x=5,
			y=5,
		)

	""" Load the world from the savefile """
	@staticmethod
	def load_() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->load_() -> StateResult")
		with open("savefile.sav", "rb") as f:
			g.world = pickle.loads(f.read())
		return Reset(InGame())

	""" Save the world and clear the world """
	@staticmethod
	def save_() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->save_() -> StateResult")
		with open("savefile.sav", "wb") as f:
			f.write(pickle.dumps(g.world))
		del(g.world)
		return Reset(MainMenu())

	@staticmethod
	def continue_() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->continue_() -> StateResult")
		return Reset(InGame())

	@staticmethod
	def new_game() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->new_game() -> StateResult")
		g.world = game.world_tools.new_world()
		# Clear g.world for all states and add InGame states
		return Reset(InGame())
	
	@staticmethod
	def quit() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->quit() -> StateResult")
		raise SystemExit
