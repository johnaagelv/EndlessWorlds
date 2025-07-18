from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import TEventHandler

if TYPE_CHECKING:
	from entities import TEntity
	from worlds import TWorld

class TEngine:
	world: TWorld

	def __init__(self, player: TEntity):
		self.event_handler: TEventHandler = TEventHandler(actor=player)
		self.player = player

	def handle_enemy_turns(self) -> None:
		# Not used
		pass

	def update_fov(self) -> None:
		# Not used, player is handling FOV or rather FOS
		pass
