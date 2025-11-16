from __future__ import annotations

from typing import Tuple

import attrs
import tcod.console
import tcod.event

@attrs.define()
class ActorState:
	"""
	State for a player character (PC) or a non-player character (NPC)
	- x, y are the coordinates in the current map
	- is_alive is alive/dead indicator
	"""
	x: int
	y: int
	is_alive: bool = True
	colour: Tuple[int, int, int] = (255, 255, 255)

	def on_draw(self, console: tcod.console.Console) -> None:
		""" ON_DRAW - draw this PC on the specified console during this draw cycle """
		console.print(self.x, self.y, "@", fg=self.colour)
	
	def on_event(self, event: tcod.event.Event) -> None:
		""" ON_EVENT - handle client event for this PC """
		match event:
			case tcod.event.Quit():
				self.is_alive = False
			case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
				self.x -= 1
			case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
				self.x += 1
			case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
				self.y -= 1
			case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
				self.y += 1
