from typing import Any, Iterable, Set
from tcod.context import Context
from tcod.console import Console

from actions import TEscapeAction, TMoveAction
from entities import TEntity
from input_handlers import TEventHandler

class TEngine:
	def __init__(self, entities: Set[TEntity], event_handler: TEventHandler):
		self.entities = entities
		self.event_handler = event_handler

	def handle_events(self, events: Iterable[Any]) -> None:
		for event in events:
			action = self.event_handler.dispatch(event)

			if action is None:
				continue
				
			action.run(self.entities[0])
	
	def render(self, console: Console, context: Context) -> None:
		for entity in self.entities:
			console.print(entity.data["x"], entity.data["y"], entity.data["face"], fg = entity.data["colour"])
		
		context.present(console)
		console.clear()
