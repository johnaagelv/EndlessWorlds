""" Derived states used in the game """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

from typing import Dict, List
import os.path
import pickle
import attrs
import tcod.console
import tcod.event
from tcod.ecs import Registry
import json
from tcod.event import KeySym

import g
from game.tags import IsPlayer, IsItem, IsActor, IsInventory
from game.constants import DIRECTION_KEYS
import game.components as gc
from game.state import Pop, Push, Reset, State, StateResult
import game.menus
import game.world_tools
import colours

import numpy as np
import tile_types

""" Primary in-game state """
@attrs.define()
class InGame(State):

	""" Draw the map """
	def _draw_map(self, console: tcod.console.Console) -> None:
		map: np.ndarray
		visible: np.ndarray
		explored: np.ndarray
		for entity in g.world.Q.all_of(components=[gc.ExplorationMemory]):
			map = entity.components[gc.ExplorationMemory].map
			visible = entity.components[gc.ExplorationMemory].visible
			explored = entity.components[gc.ExplorationMemory].explored

		console.rgb[0:80,0:50] = np.select(
			condlist=[visible, explored],
			choicelist=[map['light'], map['dark']],
			default=tile_types.SHROUD
		)

	""" Draw all the items """
	def _draw_items(self, console: tcod.console.Console) -> None:
		for entity in g.world.Q.all_of(components=[gc.Position, gc.Graphic], tags=[IsItem]):
			pos = entity.components[gc.Position]
			if not (0 <= pos.x < console.width and 0 <= pos.y < console.height):
				continue
			graphic = entity.components[gc.Graphic]
			console.rgb[["ch", "fg"]][pos.x, pos.y] = graphic.ch, graphic.fg

	""" Draw all the actors, including the player """
	def _draw_actors(self, console: tcod.console.Console) -> None:
		for entity in g.world.Q.all_of(components=[gc.Position, gc.Graphic], tags=[IsActor]):
			pos = entity.components[gc.Position]
			if not (0 <= pos.x < console.width and 0 <= pos.y < console.height):
				continue
			graphic = entity.components[gc.Graphic]
			console.rgb[["ch", "fg"]][pos.x, pos.y] = graphic.ch, graphic.fg

		(player,) = g.world.Q.all_of(tags=[IsPlayer])
		pos = player.components[gc.Position]
		graphic = player.components[gc.Graphic]
		console.rgb[["ch", "fg"]][pos.x, pos.y] = graphic.ch, graphic.fg

	""" Draw the actor's states """
	def _draw_states(self, console: tcod.console.Console) -> None:
		state_keys = [gc.Health, gc.Energy, gc.Strength]
		(player,) = g.world.Q.all_of(tags=[IsPlayer])
		view_width = 20
		view_x = console.width - view_width - 1 # TODO: Values from configuration
		view_y = 1
		for state_key in state_keys:
			current_name = player.components[state_key].__class__.__name__
			current_value = int(player.components[state_key].value / 1000)
			bar_width = int(float(player.components[state_key].value) / 1000000 * view_width)
			bar_filled = colours.bar_low
			if player.components[state_key].value > player.components[state_key].high:
				bar_filled = colours.bar_high
			elif player.components[state_key].value > player.components[state_key].medium:
				bar_filled = colours.bar_medium

			console.draw_rect(x=view_x, y=view_y, width=view_width, height=1, ch=1, bg=colours.bar_empty)
			if bar_width > 0:
				console.draw_rect(x=view_x, y=view_y, width=bar_width, height=1, ch=1, bg=bar_filled)
			console.print(x=view_x + 1, y=view_y, text=current_name, fg=colours.bar_text)
			state_x = view_width - 2 - (current_value > 9) - (current_value > 99) - (current_value > 999)
			console.print(x=view_x + state_x, y=view_y, text=str(current_value), fg=colours.bar_text)
			view_y += 1

	""" Draw the messages from the messagelog """
	def _draw_messages(self, console: tcod.console.Console) -> None:
		view_x = 1
		view_width = 58
		view_height = 6
		view_y = console.height - view_height - 1
		
		g.messages.render(console, view_x, view_y, view_width, view_height)

	""" Main game drawing method """
	def on_draw(self, console: tcod.console.Console) -> None:
		logger.info("InGame(State)->on_draw( console ) -> None")
		self._draw_map(console)
		self._draw_items(console)
		self._draw_actors(console)
		self._draw_states(console)
		self._draw_messages(console)

	""" Affects other states """
	def apply_impact(self, main_state, impact_state):
		(player,) = g.world.Q.all_of(tags=[IsPlayer])
		energy = player.components[main_state]
		impacts = player.components[impact_state]
		for affected_state in impacts.impacts:
			if player.components[affected_state].value > energy.value:
				affected_impact = (0 <= energy.value < energy.low) * impacts.low + (energy.low <= energy.value < energy.medium) * impacts.medium + (energy.medium <= energy.value < energy.high) * impacts.high
				player.components[affected_state] += affected_impact

	""" Handle events for the in-game state (game ticks) """
	def on_event(self, event: tcod.event.Event) -> StateResult:
		logger.info("InGame(State)->on_event( event ) -> StateResult")
		# Get the player
		(player,) = g.world.Q.all_of(tags=[IsPlayer])
		inventory = player.components[gc.Inventory].registry

		self.apply_impact(gc.Energy, gc.EnergyImpacts)
		self.apply_impact(gc.Health, gc.HealthImpacts)
		self.apply_impact(gc.Strength, gc.StrengthImpacts)
		match event:
			case tcod.event.Quit():
				# TODO: Ask user to confirm
				raise SystemExit
			case tcod.event.KeyDown(sym=sym) if sym in DIRECTION_KEYS:
				player.components[gc.Position] += DIRECTION_KEYS[sym]
				player.components[gc.Energy] += player.components[gc.EnergyUsage].value

			case tcod.event.KeyDown(sym=tcod.event.KeySym.I):
				return Push(InventoryMenu())

			case tcod.event.KeyDown(sym=tcod.event.KeySym.COMMA):
				# Manually pick up the item
				inventory_max_count = player.components[gc.Inventory].slots
				for item in g.world.Q.all_of(tags=[player.components[gc.Position], IsItem]):
					if gc.Gold in item.components:
						player.components[gc.Gold] += item.components[gc.Gold].value
						g.messages.add(f"Picked up {item.components[gc.Gold].value} gold", colours.white)
						item.clear()

					elif gc.Food in item.components:
						inventory_items = inventory.Q.all_of(components=[gc.IsA],tags=[IsItem]).get_entities()
						if len(inventory_items) >= inventory_max_count:
							g.messages.add("No free space", colours.orangered)
							continue
						inventory_item = inventory[object()]
						inventory_item.components[gc.Food] = gc.Food(item.components[gc.Food].value)
						inventory_item.components[gc.IsA] = gc.IsA("Food")
						inventory_item.tags |= {IsItem}

						g.messages.add("Picked up a food parcel", colours.white)
						item.clear()
					else:
						pass # Unknown command, so do nothing
				return None
			
			case tcod.event.KeyDown(sym=KeySym.ESCAPE):
				return Push(MainMenu())

			case _:
				return None

""" Inventory menu """
class InventoryMenu(game.menus.ListMenu):
	__slots__ = ()
	def __init__(self) -> None:
		logger.info("InvetoryMenu(game.menus.ListMenu)->__init__() -> None")
		menu_items: List = []
		# Get the player
		(player,) = g.world.Q.all_of(tags=[IsPlayer])

		inventory = player.components[gc.Inventory].registry
		choices = inventory.Q.all_of(components=[gc.IsA])
		for item in choices:
			if gc.Food in item.components:
				current_name = "Food parcel"
				current_value = int(item.components[gc.Food].value / 1000)

			menu_items.append(game.menus.SelectItem(current_name, current_value, self.on_select))

		menu_items.append(game.menus.SelectItem("Cancel", None, self.on_cancel))

		super().__init__(
			items=tuple(menu_items),
			selected=0,
			x=25,
			y=8,
			title="Inventory"
		)

	def on_select(self) -> StateResult:
		g.messages.add(f"Doing something with something [{self.selected}]", colours.darkgreen)
		return Pop()

	@staticmethod
	def on_cancel() -> StateResult:
		return Pop()

""" Known worlds menu """
class KnownWorldsMenu(game.menus.ListMenu):
	__slots__ = ()
	def __init__(self) -> None:
		logger.info("KnownWorldsMenu(game.menus.ListMenu)->__init__() -> None")

		menu_items: List = []
		known_worlds_filename = "known_worlds.json"
		# Check that a savefile exists
		if os.path.exists(known_worlds_filename):
			with open(known_worlds_filename, "rt") as f:
				known_worlds = json.load(f)
			
			for known_world in known_worlds['worlds']:
				menu_items.append( game.menus.SelectItem(known_world['name'], None, self.on_select))

		menu_items.append(game.menus.SelectItem("Cancel", None, self.on_cancel))

		super().__init__(
			items=tuple(menu_items),
			selected=0,
			x=5,
			y=5,
			title=None
		)

	def on_select(self) -> StateResult:
		g.messages.add(f"Initiating world [{self.selected}]", colours.darkblue)
		return Reset(MainMenu())
	
	@staticmethod
	def on_cancel() -> StateResult:
		return Reset(MainMenu())


""" Main/escape menu """
class MainMenu(game.menus.ListMenu):
	__slots__ = ()
	def __init__(self) -> None:
		logger.info("MainMenu(game.menus.ListMenu)->__init__() -> None")
		menu_items = [
			game.menus.SelectItem("Choose world", None, self.choose_known_world),
			game.menus.SelectItem("New game", None, self.new_game),
		]
		# Check that a savefile exists
		if os.path.exists('savefile.sav'):
			menu_items.append(game.menus.SelectItem("Load game", None, self.load_))

		if hasattr(g, "world"):
			menu_items.append(game.menus.SelectItem("Continue", None, self.continue_))
			menu_items.append(game.menus.SelectItem("Save", None, self.save_))

		menu_items.append(game.menus.SelectItem("Quit", None, self.quit))

		super().__init__(
			items=tuple(menu_items),
			selected=0,
			x=5,
			y=5,
			title=None
		)

	""" Load the world from the savefile """
	@staticmethod
	def load_() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->load_() -> StateResult")
		g.messages.add(f"Loading saved game", colours.darkgreen)
		with open("savefile.sav", "rb") as f:
			g.world = pickle.loads(f.read())
		return Reset(InGame())

	""" Save the world and clear the world """
	@staticmethod
	def save_() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->save_() -> StateResult")
		g.messages.add(f"Saving game", colours.darkgreen)
		with open("savefile.sav", "wb") as f:
			f.write(pickle.dumps(g.world))
		del(g.world)
		return Reset(MainMenu())

	@staticmethod
	def continue_() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->continue_() -> StateResult")
		return Reset(InGame())

	@staticmethod
	def choose_known_world() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->choose_known_world() -> StateResult")
		return Reset(KnownWorldsMenu())
	
	@staticmethod
	def new_game() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->new_game() -> StateResult")
		g.messages.add(f"Starting a new game", colours.darkgreen)
		g.world = game.world_tools.new_world()
		# Clear g.world for all states and add InGame states
		return Reset(InGame())
	
	@staticmethod
	def quit() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->quit() -> StateResult")
		raise SystemExit
