""" Base classes for game states """
from __future__ import annotations

from typing import Protocol, TypeAlias

import attrs
import tcod.console
import tcod.event

#import client.configuration as config
#import logging
#logger = logging.getLogger(config.LOG_NAME)

class State(Protocol):
	""" Abstract game state class """

	__slots__ = ()

	def on_draw(self, console: tcod.console.Console) -> None:
		""" Draw the state """
#		logger.debug("State->on_draw( console ) -> None")
		return None
	
	def on_event(self, event: tcod.event.Event) -> StateResult:
		""" Process event for the state """
#		logger.debug("State->on_event( event ) -> StateResult")
		return None

	def on_connect(self) -> StateResult:
		""" Connect with server for command processing """
#		logger.debug("State->on_connect() -> StateResult")
		return None

@attrs.define()
class Push:
	""" Push a new state on top of the stack """
	state: State

@attrs.define()
class Pop:
	""" Remove the current state from the stack """

@attrs.define()
class Reset:
	""" Replace the entire stack with a new state """
	state: State

StateResult: TypeAlias = "Push | Pop | Reset | None"
""" Union of state results """