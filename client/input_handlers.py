from typing import Optional
import tcod.event

from actions import TAction, TEscapeAction, TMoveAction

class TEventHandler(tcod.event.EventDispatch[TAction]):
	def ev_quit(self, event: tcod.event.Quit) -> Optional[TAction]:
		raise SystemExit()
	
	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[TAction]:
		action: Optional[TAction] = None

		key = event.sym

		if key == tcod.event.``