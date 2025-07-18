from __future__ import annotations

from typing import Final, Self, TYPE_CHECKING

import attrs

if TYPE_CHECKING:
	from engines import TEngine
	from entities import TEntity

class TBaseComponent:
	entity: TEntity

	@property
	def engine(self) -> TEngine:
		return self.entity.world.engine