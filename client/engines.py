from typing import Any, Iterable

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entities import TEntity
from game_map import TGameMap
from input_handlers import TEventHandler
from renders import render_bar

"""
Engine takes care of handling input and output
"""
class TClientEngine:
	def __init__(
		self,
		player: TEntity,
		event_handler: TEventHandler,
		game_map: TGameMap
	):
		self.actor = player
		self.event_handler = event_handler
		self.game_map = game_map
		self.update_fov()

	"""
	Handle the keyboard events turning them into actions
	"""
	def handle_events(
		self,
		events: Iterable[Any]
	) -> None:
		self.actor.run()
		for event in events:
			action = self.event_handler.dispatch(event)
			if action is None:
				continue				
			action.run(self.actor, self.game_map)
			self.update_fov()

	def update_fov(self) -> None:
		self.game_map.visible[:] = compute_fov(
			self.game_map.tiles["transparent"],
			(self.actor.data["location"]["x"], self.actor.data["location"]['y']),
			radius=self.actor.data["senses"]["vision"]["value"], # TODO! Take this from the player entity data
		)
		self.game_map.explored |= self.game_map.visible

	"""
	Render the map, the NPCs, and the player
	"""
	def render(
		self,
		console: Console,
		context: Context
	) -> None:
		self.game_map.render(console)
		console.print(
			self.actor.data["location"]["x"],
			self.actor.data["location"]["y"],
			self.actor.data["character"]["face"],
			fg=self.actor.data["character"]["colour"]
		)
		context.present(console)
		console.clear()
