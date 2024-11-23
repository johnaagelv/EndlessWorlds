from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console

import exceptions
from message_log import TMessageLog
import renders

import lzma
import pickle

if TYPE_CHECKING:
	from entity import TActor
	from game_map import TWorld

class TEngine:
	game_world: TWorld
	game_name: str = "<Unknown>"

	def __init__(self, player: TActor):
		self.message_log = TMessageLog()
		self.mouse_location = (0, 0)
		self.player = player
		player.parent = self

	def handle_enemy_turns(self) -> None:
		for entity in set(self.game_world.actors): # - {self.player}:
			if entity.ai:
				try:
					entity.ai.perform()
				except exceptions.Impossible:
					pass

	def update_fov(self) -> None:
		self.game_world.update_fov()

	def render(self, console: Console) -> None:
		self.game_world.render(console)
		self.player.render(console)

		self.message_log.render(console=console, x=21, y=45, width=40, height=5)

		renders.render_bar(console=console, current_value=self.player.fighter.hp, maximum_value=self.player.fighter.max_hp, total_width=20)
		renders.render_dungeon_level(console=console, dungeon_level=self.game_world.current_floor, location=(0, 47))
		renders.render_names_at_mouse_location(console=console, x=21, y=44, engine=self)
		renders.render_stairs(console=console, location=(0,48), engine=self)

	def save_as(self, filename: str) -> None:
		"""
		Save this Engine instance as a compressed file
		"""
		save_data = lzma.compress(pickle.dumps(self))
		with open(filename, "wb") as f:
			f.write(save_data)