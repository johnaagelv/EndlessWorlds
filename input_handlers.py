from __future__ import annotations
import os
from typing import Callable, Optional, Tuple, TYPE_CHECKING, Union

import tcod.event
import tcod.libtcodpy as tcodformat

from actions import TAction, TBumpAction, TDropItem, TPickupAction, TWaitAction, TTakeDownStairsAction, TTakeUpStairsAction
import colours as colour
import exceptions

if TYPE_CHECKING:
	from engine import TEngine
	from entity import TItem

MOVE_KEYS = {
	# Arrow keys.
	tcod.event.KeySym.UP: (0, -1),
	tcod.event.KeySym.DOWN: (0, 1),
	tcod.event.KeySym.LEFT: (-1, 0),
	tcod.event.KeySym.RIGHT: (1, 0),
	tcod.event.KeySym.HOME: (-1, -1),
	tcod.event.KeySym.END: (-1, 1),
	tcod.event.KeySym.PAGEUP: (1, -1),
	tcod.event.KeySym.PAGEDOWN: (1, 1),
	# Numpad keys.
	tcod.event.KeySym.KP_1: (-1, 1),
	tcod.event.KeySym.KP_2: (0, 1),
	tcod.event.KeySym.KP_3: (1, 1),
	tcod.event.KeySym.KP_4: (-1, 0),
	tcod.event.KeySym.KP_6: (1, 0),
	tcod.event.KeySym.KP_7: (-1, -1),
	tcod.event.KeySym.KP_8: (0, -1),
	tcod.event.KeySym.KP_9: (1, -1),
	# Vi keys.
	tcod.event.KeySym.h: (-1, 0),
	tcod.event.KeySym.j: (0, 1),
	tcod.event.KeySym.k: (0, -1),
	tcod.event.KeySym.l: (1, 0),
	tcod.event.KeySym.y: (-1, -1),
	tcod.event.KeySym.u: (1, -1),
	tcod.event.KeySym.b: (-1, 1),
	tcod.event.KeySym.n: (1, 1),
}

WAIT_KEYS = {
	tcod.event.KeySym.PERIOD,
	tcod.event.KeySym.KP_5,
	tcod.event.KeySym.CLEAR,
}

# Scroll UP/DOWN keys
CURSOR_Y_KEYS = {
	tcod.event.KeySym.UP: -1,
	tcod.event.KeySym.DOWN: 1,
	tcod.event.KeySym.PAGEUP: -10,
	tcod.event.KeySym.PAGEDOWN: 10,
}

SWITCH_UI_KEYS = {
	tcod.event.KeySym.v: 0,
}

CONFIRM_KEYS = {
	tcod.event.KeySym.RETURN,
	tcod.event.KeySym.KP_ENTER,
}

ActionOrHandler = Union[TAction, "TBaseEventHandler"]
"""
An event handler return value which can trigger an action or switch active handler
If a handler is returned then it will become the active handler
If an action is returned it will be attempted
"""
class TBaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
	def handle_events(self, event: tcod.event.Event) -> TBaseEventHandler:
		"""
		Handle an event and return the next active event handler
		"""
		state = self.dispatch(event)
		if isinstance(state, TBaseEventHandler):
			return state
		assert not isinstance(state, TAction), f"{self!r} can not handle actions"
		return self

	def on_render(self, console: tcod.console.Console) -> None:
		raise NotImplementedError()

	def ev_quit(self, event: tcod.event.Quit) -> Optional[TAction]:
		raise SystemExit()

class TPopupMessage(TBaseEventHandler):
	"""
	Display a popup text dialogue
	"""
	def __init__(self, parent_handler: TBaseEventHandler, text: str):
		self.parent = parent_handler
		self.text = text
	
	def on_render(self, console: tcod.console.Console) -> None:
		"""
		Render the parent and dim the result, then print the message on top
		"""
		self.parent.on_render(console)
		console.rgb["fg"] //= 8
		console.rgb["bg"] //= 8
		console.print(
			console.width // 2,
			console.height // 2,
			self.text,
			fg=colour.white,
			bg=colour.black,
			alignment=tcodformat.CENTER,
		)

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[TBaseEventHandler]:
		return self.parent # Return the handler

class TEventHandler(TBaseEventHandler):
	def __init__(self, engine: TEngine):
		self.engine = engine

	def handle_events(self, event: tcod.event.Event) -> TBaseEventHandler:
		action_or_state = self.dispatch(event)
		if isinstance(action_or_state, TBaseEventHandler):
			return action_or_state
		if self.handle_action(action_or_state):
			if not self.engine.player.is_alive:
				return TGameOverEventHandler(self.engine)
			return TMainGameEventHandler(self.engine)
		return self

	def handle_action(self, action: Optional[TAction]) -> bool:
		"""
		Handle actions returned from event methods
		Returns True if the action will advance a turn
		"""
		if action is None:
			return False
		try:
			action.perform()
		except exceptions.Impossible as exc:
			self.engine.message_log.add_message(exc.args[0], colour.impossible)
			return False
		self.engine.handle_enemy_turns()
		self.engine.update_fov()
		return True

	def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
		if self.engine.game_world.in_bounds(event.tile.x, event.tile.y):
			self.engine.mouse_location = event.tile.x, event.tile.y

	def on_render(self, console: tcod.console.Console) -> None:
		self.engine.render(console)

class TMainGameEventHandler(TEventHandler):
	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
		action: Optional[TAction] = None

		key = event.sym
		modifier = event.mod

		player = self.engine.player

		if key == tcod.event.KeySym.PERIOD and modifier & (tcod.event.Modifier.LSHIFT | tcod.event.Modifier.RSHIFT):
			return TTakeDownStairsAction(player)

		if key == tcod.event.KeySym.COMMA and modifier & (tcod.event.Modifier.LSHIFT | tcod.event.Modifier.RSHIFT):
			return TTakeUpStairsAction(player)

		if key in MOVE_KEYS:
			dx, dy = MOVE_KEYS[key]
			action = TBumpAction(player, dx, dy)
		elif key in WAIT_KEYS:
			action = TWaitAction(player)

		elif key == tcod.event.KeySym.ESCAPE:
			raise SystemExit()
		elif key in SWITCH_UI_KEYS:
			return THistoryViewer(self.engine)

		# Item pickup
		elif key == tcod.event.KeySym.g:
			action = TPickupAction(player)

		# Inventory
		elif key == tcod.event.KeySym.i:
			return TInventoryActivateHandler(self.engine)
		elif key == tcod.event.KeySym.d:
			return TInventoryDropHandler(self.engine)
		elif key == tcod.event.KeySym.SLASH:
			return TLookHandler(self.engine)

		# No valid key was pressed
		return action

class TGameOverEventHandler(TEventHandler):
	def on_quit(self) -> None:
		if os.path.exists("savegame.sav"):
			os.remove("savegame.sav")
		raise exceptions.QuitWithoutSaving()

	def ev_quit(self, event: tcod.event.Quit) -> None:
		"""
		Handle when closing the window
		"""
		self.on_quit()

	def ev_keydown(self, event: tcod.event.KeyDown) -> None:
		"""
		Handle when using Escape to end the game
		"""
		if event.sym == tcod.event.KeySym.ESCAPE:
			self.on_quit()

class THistoryViewer(TEventHandler):
	""" print the history on a larger window with up/down scrolling """
	def __init__(self, engine: TEngine):
		super().__init__(engine)
		self.log_length = len(engine.message_log.messages)
		self.cursor = self.log_length - 1
	
	def on_render(self, console: tcod.console.Console) -> None:
		super().on_render(console)

		log_console = tcod.console.Console(console.width -6, console.height - 6)

		log_console.draw_frame(0, 0, log_console.width, log_console.height)
		log_console.print_box(0, 0, log_console.width, 1, "|Message history|", alignment=tcodformat.CENTER)

		self.engine.message_log.render_messages(log_console, 1, 1, log_console.width - 2, log_console.height - 2, self.engine.message_log.messages[: self.cursor + 1])
		log_console.blit(console, 3, 3)

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
		if event.sym in CURSOR_Y_KEYS:
			adjust = CURSOR_Y_KEYS[event.sym]
			if adjust < 0 and self.cursor == 0:
				self.cursor = self.log_length - 1
			elif adjust > 0 and self.cursor == self.log_length - 1:
				self.cursor = 0
			else:
				self.cursor = max(0, min(self.cursor + adjust, self.log_length -1))
		elif event.sym == tcod.event.KeySym.HOME:
			self.cursor = 0
		elif event.sym == tcod.event.KeySym.END:
			self.cursor = self.log_length - 1
		else:
			return TMainGameEventHandler(self.engine)
		return None

class TAskUserEventHandler(TEventHandler):
	"""
	Handles user input for actions which require special input
	"""
	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
		if event.sym in {
			tcod.event.KeySym.LSHIFT,
			tcod.event.KeySym.RSHIFT,
			tcod.event.KeySym.LCTRL,
			tcod.event.KeySym.RCTRL,
			tcod.event.KeySym.LALT,
			tcod.event.KeySym.RALT,
		}:
			return None
		return self.on_exit()

	def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
		return self.on_exit()
	
	def on_exit(self) -> Optional[ActionOrHandler]:
		return TMainGameEventHandler(self.engine)

class TInventoryEventHandler(TAskUserEventHandler):
	"""
	This handler lets the user select an item
	"""
	TITLE = "<missing title>"

	def on_render(self, console: tcod.console.Console) -> None:
		"""
		Render an inventory menu, which displays the items in the inventory, 
		and the letter to select them. Will move to a different position based
		on where the player is located, so the player can always see where
		they are.
		"""
		super().on_render(console)
		number_of_items_in_inventory = len(self.engine.player.inventory.items)

		height = number_of_items_in_inventory + 2
		if height <= 3:
			height = 3
		if self.engine.player.x <= 30:
			x = 40
		else:
			x = 0
		y = 0
		width = len(self.TITLE) + 4

		console.draw_frame(
			x=x,
			y=y,
			width=width,
			height=height,
			title=self.TITLE,
			clear=True,
			fg=(255, 255, 255),
			bg=(0, 0, 0),
		)
		if number_of_items_in_inventory > 0:
			for i, item in enumerate(self.engine.player.inventory.items):
				item_key = chr(ord("a") + i)
				console.print(x + 1, y + i + 1, f"({item_key}) {item.name}")
		else:
			console.print(x + 1, y + 1, "(Empty)")

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
		player = self.engine.player
		key = event.sym
		index = key - tcod.event.KeySym.a
		# 01234567890123456789012345
		# abcdefghijklmnopqrstuvwxyz
		if 0 <= index < 26:
			try:
				selected_item = player.inventory.items[index]
			except IndexError:
				self.engine.message_log.add_message("Uh??", colour.invalid)
				return None
			return self.on_item_selected(selected_item)
		return super().ev_keydown(event)
	
	def on_item_selected(self, item: TItem) -> Optional[ActionOrHandler]:
		"""
		Called when the user selects a valid item
		"""
		raise NotImplementedError()

class TInventoryActivateHandler(TInventoryEventHandler):
	"""
	Handle using an inventory item
	"""
	TITLE = "Select an item to use"

	def on_item_selected(self, item: TItem) -> Optional[ActionOrHandler]:
		return item.consumable.get_action(self.engine.player)
	
class TInventoryDropHandler(TInventoryEventHandler):
	"""
	Handle dropping an inventory item
	"""
	TITLE = "Select an item to drop"

	def on_item_selected(self, item: TItem) -> Optional[ActionOrHandler]:
		return TDropItem(self.engine.player, item)

class TSelectIndexHandler(TAskUserEventHandler):
	"""
	Handles asking the user for an index on the map
	"""
	def __init__(self, engine: TEngine):
		"""
		Sets the cursor to the player when instantiated
		"""
		super().__init__(engine)
		player = self.engine.player
		engine.mouse_location = player.x, player.y

	def on_render(self, console: tcod.console.Console) -> None:
		"""
		Highlight the tile under the cursor
		"""
		super().on_render(console)
		x, y = self.engine.mouse_location
		console.rgb["bg"][x, y] = colour.white
		console.rgb["fg"][x, y] = colour.black

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
		"""
		Check for key movement or confirmation keys
		"""
		key = event.sym
		if key in MOVE_KEYS:
			modifier = 1
			if event.mod & (tcod.event.Modifier.LSHIFT | tcod.event.Modifier.RSHIFT):
				modifier = 5
			if event.mod & (tcod.event.Modifier.LCTRL | tcod.event.Modifier.RCTRL):
				modifier = 10
			if event.mod & (tcod.event.Modifier.LALT | tcod.event.Modifier.RALT):
				modifier = 20

			x, y = self.engine.mouse_location
			dx, dy = MOVE_KEYS[key]
			x += dx * modifier
			y += dy * modifier
			# Keep the cursor index within the map
			x = max(0, min(x, self.engine.game_world.maps[self.engine.game_world.current_floor].width - 1))
			y = max(0, min(y, self.engine.game_world.maps[self.engine.game_world.current_floor].height - 1))
			self.engine.mouse_location = x, y
			return None
		elif key in CONFIRM_KEYS:
			return self.on_index_selected(*self.engine.mouse_location)
		return super().ev_keydown(event)

	def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
		"""
		Left click confirms a selection
		"""
		if self.engine.game_world.maps[self.engine.game_world.current_floor].in_bounds(*event.tile):
			if event.button == 1:
				return self.on_index_selected(*event.tile)
		return super().ev_mousebuttondown(event)

	def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
		raise NotImplementedError()

class TLookHandler(TSelectIndexHandler):
	"""
	Lets the player look around using the keyboard
	"""
	def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
		return TMainGameEventHandler(self.engine)

class TSingleRangedAttackHandler(TSelectIndexHandler):
	"""
	Handles targeting a single enemy
	"""
	def __init__(self, engine: TEngine, callback: Callable[[Tuple[int, int]], Optional[TAction]]):
		super().__init__(engine)
		self.callback = callback

	def on_index_selected(self, x: int, y: int) -> Optional[TAction]:
		return self.callback((x, y))

class TAreaRangedAttachHandler(TSelectIndexHandler):
	"""
	Handles targeting an area within a given radius
	"""
	def __init__(self, engine: TEngine, radius: int, callback: Callable[[Tuple[int, int]], Optional[TAction]]):
		super().__init__(engine)
		self.radius = radius
		self.callback = callback
	
	def on_render(self, console: tcod.console.Console) -> None:
		super().on_render(console)
		x, y = self.engine.mouse_location
		console.draw_frame(
			x=x - self.radius - 1,
			y=y - self.radius - 1,
			width=self.radius ** 2,
			height=self.radius ** 2,
			fg=colour.red,
			clear=False,
		)
	
	def on_index_selected(self, x: int, y: int) -> Optional[TAction]:
		return self.callback((x, y))