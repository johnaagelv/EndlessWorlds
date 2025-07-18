from __future__ import annotations
from typing import Optional
import logging
logger = logging.getLogger("EWClient")

import tcod.event
from actions import TAction, TEscapeAction, TMoveAction, TStairAction
from entities import TEntity, TActor

class TEventHandler(tcod.event.EventDispatch[TAction]):
	def __init__(self, actor: TEntity):
		logger.debug(f"TEventHandler->__init__( actor )")
		self.actor = actor

	def handle_events(self) -> None:
		logger.debug(f"TEventHandler->handle_event()")
		for event in tcod.event.wait():
			action = self.dispatch(event)

			if action is None:
				continue

			action.run()

			self.actor.update_fos()

	def ev_quit(self, event: tcod.event.Quit) -> Optional[TAction]:
		logger.debug(f"TEventHandler->ev_quit( event )")
		return TEscapeAction(self.actor)
	
	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[TAction]:
		logger.debug(f"TEventHandler->ev_keydown( event )")
		action: Optional[TAction] = None
		
		key = event.sym
		logger.info(f"- key='{key}' {tcod.event.KeySym.GREATER} or {tcod.event.KeySym.LESS}")
		if key == tcod.event.KeySym.ESCAPE:
			action = TEscapeAction(self.actor)
		elif key == tcod.event.KeySym.UP:
			action = TMoveAction(self.actor, dx=0, dy=-1)
		elif key == tcod.event.KeySym.DOWN:
			action = TMoveAction(self.actor, dx=0, dy=1)
		elif key == tcod.event.KeySym.LEFT:
			action = TMoveAction(self.actor, dx=-1, dy=0)
		elif key == tcod.event.KeySym.RIGHT:
			action = TMoveAction(self.actor, dx=1, dy=0)
		elif key == 46: #tcod.event.KeySym.KP_GREATER:
			action = TStairAction(self.actor, "down")
		elif key == 44: #tcod.event.KeySym.KP_LESS:
			action = TStairAction(self.actor, "up")
		else:
			if key < 256:
				action = TStairAction(self.actor, chr(key))
			else:
				action = TMoveAction(self.actor, dx=0, dy=0, user_action=key)

		return action

#	def on_render(self, console: tcod.console.Console) -> None:
#		logger.debug(f"TEventHandler->on_render( console )")
#		self.engine.render(console)