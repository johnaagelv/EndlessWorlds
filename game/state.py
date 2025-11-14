""" Base classes for states using Protocols """
from __future__ import annotations

from typing import Protocol, TypeAlias

import attrs
import tcod.console
import tcod.event

""" Abstract game state """
class State(Protocol):
	# Placeholder for properties
	__slots__ = ()

	""" Called when the state is to be drawn (presented) """
	def on_draw(self, console: tcod.console.Console) -> None:
		...

	""" Called when the state must process events """	
	def on_event(self, event: tcod.event.Event) -> None:
		...

""" Push a new state on top of the stack """
@attrs.define()
class Push:
	state: State

""" Remove the current (top) state from the stack """
@attrs.define()
class Pop:
	...

""" Replace the entire stack with a new state """
@attrs.define()
class Reset:
	state: State

""" Union of the state results """
StateResult: TypeAlias = "Push | Pop | Reset | None"