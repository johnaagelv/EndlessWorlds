""" Menu UI classes """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

from collections.abc import Callable
from typing import Protocol

import attrs
import tcod.console
import tcod.event
from tcod.event import KeySym

import game.state_tools
from game.constants import DIRECTION_KEYS
from game.state import Pop, State, StateResult

""" Menu item protocol """
class MenuItem(Protocol):
	__slots__ = ()

	""" Handle events passed to this menu item """
	def on_event(self, event: tcod.event.Event) -> StateResult:
		pass
	
	""" Draw this item at the given position """
	def on_draw(self, console: tcod.console.Console, x: int, y: int, highlight: bool) -> None:
		pass

""" Clickable menu item """
@attrs.define()
class SelectItem(MenuItem):
	label: str
	callback: Callable[[], StateResult]

	""" Handle events selecting this menu item """
	def on_event(self, event: tcod.event.Event) -> StateResult:
		logger.info("SelectItem(MenuItem)->on_event( event ) -> StateResult")
		match event:
			case tcod.event.KeyDown(sym=sym) if sym in {KeySym.RETURN, KeySym.RETURN2, KeySym.KP_ENTER}:
				return self.callback()
			case tcod.event.MouseButtonUp(button=tcod.event.MouseButton.LEFT):
				return self.callback()
			case _:
				return None
			
	def on_draw(self, console: tcod.console.Console, x: int, y: int, highlight: bool) -> None:
		logger.info("SelectItem(MenuItem)->on_draw( console, x, y, highlight ) -> None")
		console.print(x, y, self.label, fg=(255, 255, 255), bg=(64, 64, 64) if highlight else (0, 0, 0))

""" Simple list menu state """
@attrs.define()
class ListMenu(State):
	items: tuple[MenuItem, ...]
	selected: int | None = 0
	x: int = 0
	y: int = 0

	""" Handle events for menus """
	def on_event(self, event: tcod.event.Event) -> StateResult:
		logger.info("ListMenu(State)->on_event( event ) -> StateResult")
		match event:
			case tcod.event.Quit():
				raise SystemExit
			case tcod.event.KeyDown(sym=sym) if sym in DIRECTION_KEYS:
				dx, dy = DIRECTION_KEYS[sym]
				if dx != 0 or dy == 0:
					return self.activate_selected(event)
				if self.selected is not None:
					self.selected += dy
					self.selected %= len(self.items)
				else:
					self.selected = 0 if dy == 1 else len(self.items) - 1
				return None
			case tcod.event.MouseMotion(position=(_, y)): # FLOAT returned here!
				y = int(y - self.y) # Make it an INT
				self.selected = y if 0 <= y < len(self.items) else None
				return None
			case tcod.event.KeyDown(sym=KeySym.ESCAPE):
				return self.on_cancel()
			case tcod.event.MouseButtonUp(button=tcod.event.MouseButton.RIGHT):
				return self.on_cancel()
			case _:
				return self.activate_selected(event)

	""" Call the selected menu item's callback """
	def activate_selected(self, event: tcod.event.Event) -> StateResult:
		logger.info("ListMenu(State)->activate_selected( event ) -> StateResult")
		if self.selected is not None:
			return self.items[self.selected].on_event(event)
		return None
	
	""" Handle escape or right click being selected on the menu """
	def on_cancel(self) -> StateResult:
		logger.info("ListMenu(State)->on_cancel() -> StateResult")
		return Pop()
	
	""" Render the menu """
	def on_draw(self, console: tcod.console.Console) -> None:
		logger.info("ListMenu(State)->on_draw( console ) -> None")
		game.state_tools.draw_previous_state(self, console)
		for i, item in enumerate(self.items):
			item.on_draw(console, x=self.x, y=self.y + i, highlight=i == self.selected)

