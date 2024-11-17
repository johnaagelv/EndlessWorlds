from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import TMainGameEventHandler
from message_log import TMessageLog
from renders import render_bar, render_names_at_mouse_location

if TYPE_CHECKING:
	from entity import TActor
	from game_map import TGameMap
	from input_handlers import TEventHandler


class TEngine:
	game_map: TGameMap

	def __init__(self, player: TActor):
		self.event_handler: TEventHandler = TMainGameEventHandler(self)
		self.message_log = TMessageLog()
		self.mouse_location = (0, 0)
		self.player = player

	def handle_enemy_turns(self) -> None:
		for entity in set(self.game_map.actors) - {self.player}:
			if entity.ai:
				entity.ai.perform()

	def update_fov(self) -> None:
		"""Recompute the visible area based on the players point of view."""
		self.game_map.visible[:] = compute_fov(
			self.game_map.tiles["transparent"],
			(self.player.x, self.player.y),
			radius=8,
		)
		# If a tile is "visible" it should be added to "explored".
		self.game_map.explored |= self.game_map.visible

	def render(self, console: Console) -> None:
		self.game_map.render(console)

		self.message_log.render(console=console, x=21, y=45, width=40, height=5)

		render_bar(console=console, current_value=self.player.fighter.hp, maximum_value=self.player.fighter.max_hp, total_width=20)

		render_names_at_mouse_location(console=console, x=21, y=44, engine=self)