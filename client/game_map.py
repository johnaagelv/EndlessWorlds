from __future__ import annotations
from typing import Iterable, TYPE_CHECKING

import numpy as np
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
	from entities import TEntity

class TGameMap:
	def __init__(self, width: int, height: int, entities: Iterable[TEntity] = ()):
		self.width, self.height = width, height
		self.entities = set(entities)
		self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

		self.visible = np.full((width, height), fill_value=False, order="F")
		self.explored = np.full((width, height), fill_value=False, order="F")
	
	def in_bounds(self, x: int, y: int) -> bool:
		return 0 <= x < self.width and 0 <= y < self.height
	
	def render(self, console: Console) -> None:
		console.rgb[0:self.width, 0:self.height] = np.select(
			condlist=[self.visible, self.explored],
			choicelist=[self.tiles["light"], self.tiles["dark"]],
			default=tile_types.SHROUD
		)

		for entity in self.entities:
			if self.visible[entity.x, entity.y]:
				console.print(x=entity["location"]["x"], y=entity["location"]["y"], string=entity["character"]["face"], fg=entity.data["character"]["colour"])