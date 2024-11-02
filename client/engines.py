from typing import Any, Iterable, Set
from tcod.context import Context
from tcod.console import Console

from entities import TEntity
from game_map import TGameMap
from input_handlers import TEventHandler

class TEngine:
	def __init__(
		self,
		player: TEntity,
		event_handler: TEventHandler,
		game_map: TGameMap
	):
		self.entity = player
		self.event_handler = event_handler
		self.game_map = game_map

	def handle_events(
		self,
		events: Iterable[Any]
	) -> None:
		for event in events:
			action = self.event_handler.dispatch(event)
			if action is None:
				continue				
			action.run(self.entity, self.game_map)
	
	def render(
		self,
		console: Console,
		context: Context
	) -> None:
		self.game_map.render(console)
		console.print(
			self.entity.data["x"],
			self.entity.data["y"],
			self.entity.data["face"],
			fg=self.entity.data["colour"]
		)
		context.present(console)
		console.clear()
