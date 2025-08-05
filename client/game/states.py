""" Derived states used in the game """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

import time
from typing import List
import os.path
import pickle
import attrs
import tcod.console
import tcod.event
import json
from tcod.event import KeySym
from random import Random

import g
from game.tags import IsPlayer, IsItem, IsActor, IsConsumable
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
		
		# Draw other states, numeric
		item = player.components[gc.Gold]
		console.print(x=view_x, y=view_y, text=" Gold {:>13} ".format(item.value), fg=colours.gold, bg=colours.black)

	""" Draw the actor's states """
	def _draw_inventory(self, console: tcod.console.Console) -> None:
		(player,) = g.world.Q.all_of(tags=[IsPlayer])
		view_width = 20
		view_x = console.width - view_width - 1 # TODO: Values from configuration
		view_y = 5
		inventory = player.components[gc.Inventory].registry
		items = inventory.Q.all_of(components=[gc.Food])
		for item in items:
			if gc.Food in item.components:
				console.print(x=view_x, y=view_y, text=" Food {:>13} ".format(int(item.components[gc.Food].value/1000)), fg=colours.white, bg=colours.black)


	""" Draw the messages from the messagelog """
	def _draw_messages(self, console: tcod.console.Console) -> None:
		view_x = 1
		view_width = 58
		view_height = 6
		view_y = console.height - view_height - 1
		
		g.messages.render(console, view_x, view_y, view_width, view_height)

	""" Run brains """
	def _run_brains(self) -> None:
		rng = g.world[None].components[Random]
		(player,) = g.world.Q.all_of(tags=[IsPlayer])
		for npc in g.world.Q.all_of(tags=[IsActor]):
			time_diff = (time.time() - npc.components[gc.ActorTimer].start_time) * 1e3
			npc_movement = (0, 0)
			if time_diff >= rng.randint(500, 1500):
				npc.components[gc.ActorTimer] = gc.ActorTimer(time.time())
				if gc.Relationship in npc.components:
					x_diff = player.components[gc.Position].x > npc.components[gc.Position].x
					y_diff = player.components[gc.Position].y > npc.components[gc.Position].y
					npc_movement = (1 if x_diff else -1, 1 if y_diff else -1)
					if npc.components[gc.Position].x == player.components[gc.Position].x and npc.components[gc.Position].y == player.components[gc.Position].y:
						del(npc.components[gc.Relationship])
				else:
					if gc.TargetPosition in npc.components:
						x_diff = npc.components[gc.TargetPosition].x > npc.components[gc.Position].x
						y_diff = npc.components[gc.TargetPosition].y > npc.components[gc.Position].y
						npc_movement = (1 if x_diff else -1, 1 if y_diff else -1)
						if npc.components[gc.Position].x == npc.components[gc.TargetPosition].x and npc.components[gc.Position].y == npc.components[gc.TargetPosition].y:
							del(npc.components[gc.TargetPosition])
				if rng.randint(0, 100) > 95:
					npc.components[gc.TargetPosition] = gc.TargetPosition(rng.randint(1, 79), rng.randint(1, 45))

				
			npc.components[gc.Position] += npc_movement
		return None

	""" Main game drawing method """
	def on_draw(self, console: tcod.console.Console) -> None:
		logger.info("InGame(State)->on_draw( console ) -> None")
		self._draw_map(console)
		self._draw_items(console)
		self._draw_actors(console)
		self._draw_states(console)
		self._draw_inventory(console)
		self._draw_messages(console)
		self._run_brains()

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

		rng = g.world[None].components[Random]

		# Get the player
		(player,) = g.world.Q.all_of(tags=[IsPlayer])
		inventory = player.components[gc.Inventory].registry

		self.apply_impact(gc.Energy, gc.EnergyImpacts)
		self.apply_impact(gc.Health, gc.HealthImpacts)
		self.apply_impact(gc.Strength, gc.StrengthImpacts)
		time_diff = (time.time() - player.components[gc.ActorTimer].start_time) * 1e3
		match event:
			case tcod.event.Quit():
				# TODO: Ask user to confirm
				raise SystemExit
			case tcod.event.KeyDown(sym=sym) if sym in DIRECTION_KEYS:
				if time_diff >= 250.0:
					player.components[gc.ActorTimer] = gc.ActorTimer(time.time())
					player.components[gc.Position] += DIRECTION_KEYS[sym]
					player.components[gc.Energy] += player.components[gc.EnergyUsage].value

			case tcod.event.KeyDown(sym=tcod.event.KeySym.I):
				return Push(InventoryMenu())

			case tcod.event.KeyDown(sym=tcod.event.KeySym.COMMA):
				player.components[gc.ActorTimer] = gc.ActorTimer(time.time())
				# Manually pick up the item
				inventory_max_count = player.components[gc.Inventory].slots
				items = g.world.Q.all_of(components=[gc.Gold], tags=[player.components[gc.Position], IsItem]).get_entities()
				if len(items) > 0:
					item_amount = 0
					for item in items:
						player.components[gc.Gold] += item.components[gc.Gold].value
						item_amount += item.components[gc.Gold].value
						item.clear()
					g.messages.add(f"Picked up {item_amount} gold", colours.white)

				items = g.world.Q.all_of(components=[gc.Food], tags=[player.components[gc.Position], IsConsumable]).get_entities()
				if len(items) > 0:
					item_amount = 0
					inventory_items = inventory.Q.all_of(components=[gc.Food]).get_entities()
					if len(inventory_items) ==0:
						inventory_item = inventory[object()]
						inventory_item.components[gc.Food] = gc.Food(0, "food")

					(inventory_item, ) = inventory.Q.all_of(components=[gc.Food])
					for item in items:
						inventory_item.components[gc.Food] += item.components[gc.Food].value
						item_amount += item.components[gc.Food].value
						item.clear()
					g.messages.add(f"Picked up {int(item_amount/1000)} food energy", colours.white)
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
		choices = inventory.Q.all_of(tags=[IsConsumable])
#		for item in choices:
#			if gc.Food in item.components:
#				current_name = "Food parcel"
#				current_value = int(item.components[gc.Food].value / 1000)

#			menu_items.append(game.menus.SelectItem(current_name, current_value, self.on_select))

		menu_items.append(game.menus.SelectItem("Cancel", None, self.on_cancel))

		# Initialize the menu
		super().__init__(items=tuple(menu_items), selected=0, x=25, y=5, title="Inventory")

	""" Inventory item has been selected, handle it """
	def on_select(self) -> StateResult:
		selected_item = (item for idx, item in enumerate(self.items) if idx == self.selected)
		g.messages.add(f"Selected [{self.selected}], {selected_item}", colours.darkgreen)
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

		super().__init__(items=tuple(menu_items), selected=0, x=25, y=5, title=None)

	def on_select(self) -> StateResult:
		selected_item = (item for idx, item in enumerate(self.items) if idx == self.selected)
		g.messages.add(f"Initiating world '{selected_item}'", colours.darkblue)
		return Reset(MainMenu())

""" Main menu """
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

		super().__init__(items=tuple(menu_items), selected=0, x=25, y=5, title=None)

	""" Load the world from the savefile """
	@staticmethod
	def load_() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->load_() -> StateResult")
		g.messages.clear()
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
		return Reset(MainMenu())

	""" User selected to continue """
	@staticmethod
	def continue_() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->continue_() -> StateResult")
		return Reset(InGame())

	""" User selected to choose a World """
	def choose_known_world(self) -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->choose_known_world() -> StateResult")
		return Reset(KnownWorldsMenu())

	""" User selected to start a new game """
	@staticmethod
	def new_game() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->new_game() -> StateResult")
		g.messages.clear()
		g.messages.add(f"Starting a new game", colours.darkgreen)
		g.world = game.world_tools.new_world()
		# Clear g.world for all states and add InGame states
		return Reset(InGame())

	""" User selected to quit the game """
	@staticmethod
	def quit() -> StateResult:
		logger.info("MainMenu(game.menus.ListMenu)->quit() -> StateResult")
		raise SystemExit