from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event
import tcod.libtcodpy as tcodformat

from actions import TAction, TBumpAction, TEscapeAction, TWaitAction

if TYPE_CHECKING:
	from engine import TEngine

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

class TEventHandler(tcod.event.EventDispatch[TAction]):
	def __init__(self, engine: TEngine):
		self.engine = engine

	def handle_events(self, context: tcod.context.Context) -> None:
		for event in tcod.event.wait(timeout=2.0):
			context.convert_event(event)
			self.dispatch(event)

	def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
		if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
			self.engine.mouse_location = event.tile.x, event.tile.y

	def ev_quit(self, event: tcod.event.Quit) -> Optional[TAction]:
		raise SystemExit()
	
	def on_render(self, console: tcod.console.Console) -> None:
		self.engine.render(console)

class TMainGameEventHandler(TEventHandler):
	def handle_events(self, context: tcod.context.Context) -> None:
		for event in tcod.event.wait(timeout=2.0):
			context.convert_event(event)

			action = self.dispatch(event)

			if action is None:
				continue

			action.perform()

			self.engine.handle_enemy_turns()
			self.engine.update_fov()  # Update the FOV before the players next action.

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[TAction]:
		action: Optional[TAction] = None

		key = event.sym

		player = self.engine.player

		if key in MOVE_KEYS:
			dx, dy = MOVE_KEYS[key]
			action = TBumpAction(player, dx, dy)
		elif key in WAIT_KEYS:
			action = TWaitAction(player)

		elif key == tcod.event.KeySym.ESCAPE:
			action = TEscapeAction(player)
		elif key in SWITCH_UI_KEYS:
			self.engine.event_handler = THistoryViewer(self.engine)

		# No valid key was pressed
		return action

class TGameOverEventHandler(TEventHandler):
	def handle_events(self, context: tcod.context.Context) -> None:
		for event in tcod.event.wait(timeout=2.0):
			action = self.dispatch(event)

			if action is None:
				continue

			action.perform()

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[TAction]:
		action: Optional[TAction] = None

		key = event.sym

		if key == tcod.event.KeySym.ESCAPE:
			action = TEscapeAction(self.engine.player)

		# No valid key was pressed
		return action

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
	
	def ev_keydown(self, event: tcod.event.KeyDown) -> None:
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
			self.engine.event_handler = TMainGameEventHandler(self.engine)