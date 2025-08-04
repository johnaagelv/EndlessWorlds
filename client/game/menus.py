""" Menu UI classes """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

from collections.abc import Callable
from typing import Protocol, Tuple

import attrs
import g
import tcod.console
import tcod.event
from tcod.event import KeySym

#import game.state_tools
import game.systems
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

	def menu_lenght(self) -> int:
		return 0

""" Clickable menu item """
@attrs.define()
class SelectItem(MenuItem):
	label: str # Label to show in this menu item
	count: int | None # Optional count to show
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
			
	def on_draw(self, console: tcod.console.Console, x: int, y: int, highlight: bool, width: int) -> None:
		logger.info("SelectItem(MenuItem)->on_draw( console, x, y, highlight ) -> None")
		width -= 2
		label = " {:{width}} ".format(self.label, width=width)
		if self.count is not None:
			width = width - len(self.label) - 1
			number = "{:>{width}}".format(self.count, width=width)
			label = " {} {} ".format(self.label, number)

		console.print(x, y, label, fg=(255, 255, 255), bg=(0, 128, 0) if highlight else (96, 96, 96))
	
	def menu_length(self) -> int:
		width = len(self.label) + 2
		if self.count is not None:
			width += len(str(self.count)) + 1
		return width

""" Simple list menu state """
@attrs.define()
class ListMenu(State):
	items: Tuple[SelectItem, ...]
	selected: int | None = 0
	x: int = 0
	y: int = 0
	title: str | None = None

	""" Handle events for menus """
	def on_event(self, event: tcod.event.Event) -> StateResult:
		logger.info("ListMenu(State)->on_event( event ) -> StateResult")
		match event:
			case tcod.event.Quit():
				# Handle window close event
				raise SystemExit
			
			case tcod.event.KeyDown(sym=sym) if sym in DIRECTION_KEYS:
				# Handle menu navigation keys up/down
				dx, dy = DIRECTION_KEYS[sym]
				if dx != 0 or dy == 0:
					return self.activate_selected(event)
				if self.selected is not None:
					self.selected += dy
					self.selected %= len(self.items)
				else:
					self.selected = 0 if dy == 1 else len(self.items) - 1
				return None
			
			case tcod.event.MouseMotion(position=(_, y)): # MouseMotion returns a FLOAT!
				# Handle mouse position
				y = int(y - self.y) # Make it an INT
				self.selected = y if 0 <= y < len(self.items) else None
				return None

			case tcod.event.KeyDown(sym=KeySym.ESCAPE):
				# Handle Escape key
				return self.on_cancel()
			
			case tcod.event.MouseButtonUp(button=tcod.event.MouseButton.RIGHT):
				# Handle right mouse button same as Escape key
				return self.on_cancel()
			
			case _:
				# Otherwise activate the selected menu item
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
		# Draw the previous state, if any, behind the menu
		game.systems.draw_previous_state(self, console)
		inventory_width: int = 0
		for item in self.items:
			inventory_width = max(inventory_width, item.menu_length())
		self.x = int(console.width / 2 - inventory_width / 2)
		y = self.y

		if self.title is not None:
			console.print(self.x, y, text="{:^{width}}".format(self.title, width=inventory_width),fg=(255, 255, 255), bg=(64, 64, 64))
			y += 1

		console.print(self.x, y, text="{:^{width}}".format(" ", width=inventory_width),fg=(255, 255, 255), bg=(96, 96, 96))

		for i, item in enumerate(self.items):
			y += 1
			item.on_draw(console, x=self.x, y=y, highlight=i == self.selected, width=inventory_width)

		y += 1
		console.print(self.x, y, text="{:^{width}}".format(" ", width=inventory_width),fg=(255, 255, 255), bg=(96, 96, 96))
