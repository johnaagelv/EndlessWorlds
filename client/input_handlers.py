from typing import Optional
import tcod.event
from actions import TAction, TEscapeAction, TMoveAction
from entities import TActor

class TEventHandler(tcod.event.EventDispatch[TAction]):
	def __init__(self, actor: TActor):
		self.actor = actor

	def handle_events(self) -> None:
		for event in tcod.event.wait():
			action: TAction = self.dispatch(event)

			if action is None:
				continue

			action.run(self.actor)

			self.actor.update_fos()

	def ev_quit(self, event: tcod.event.Quit) -> Optional[TAction]:
		return TEscapeAction()
	
	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[TAction]:
		action: Optional[TAction] = None
		
		key = event.sym
		if key == tcod.event.KeySym.UP:
			action = TMoveAction(dx=0, dy=-1)
		elif key == tcod.event.KeySym.DOWN:
			action = TMoveAction(dx=0, dy=1)
		elif key == tcod.event.KeySym.LEFT:
			action = TMoveAction(dx=-1, dy=0)
		elif key == tcod.event.KeySym.RIGHT:
			action = TMoveAction(dx=1, dy=0)
		elif key == tcod.event.KeySym.ESCAPE:
			action = TEscapeAction()

		return action

	def on_render(self, console: tcod.console.Console) -> None:
		self.engine.render(console)
