from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from engine import TEngine
	from entity import TEntity
	from game_map import TGameMap

class TBaseComponent:
	parent: TEntity  # Owning entity instance.

	@property
	def gamemap(self) -> TGameMap:
		return self.parent.gamemap

	@property
	def engine(self) -> TEngine:
		return self.gamemap.engine
