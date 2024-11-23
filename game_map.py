from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console
from tcod.map import compute_fov

from entity import TActor, TItem
import tile_types

if TYPE_CHECKING:
	from engine import TEngine
	from entity import TEntity

class TWorld:
	"""
	Holds the settings for the gamemap and generates new maps when
	moving down/up the stairs
	"""
	def __init__(
			self,
			*,
			engine: TEngine,
			map_width: int,
			map_height: int,
			current_floor: int = 0,
	):
		self.engine = engine
		self.map_width = map_width
		self.map_height = map_height
		self.current_floor = current_floor

		self.maps = []
	
	@property
	def actors(self) -> Iterator[TActor]:
		"""Iterate over this maps living actors."""
		yield from (
			entity
			for entity in self.maps[self.current_floor]["entities"]
			if isinstance(entity, TActor) and entity.is_alive
		)

	def update_fov(self) -> None:
		"""
		Recompute the visible area based on the players point of view
		"""
		self.maps[self.current_floor]["visible"][:] = compute_fov(
			self.maps[self.current_floor]["tiles"]["transparent"],
			(self.engine.player.x, self.engine.player.y),
			radius=5,
		)
		# If a tile is "visible" it should be added to "explored".
		self.maps[self.current_floor]["explored"] |= self.maps[self.current_floor]["visible"]

	def generate_floor(self) -> None:
		from procgen import generate_dungeon
		self.maps.append(
			generate_dungeon(
				map_width = self.map_width,
				map_height = self.map_height,
				engine = self.engine,
			)
		)
		#self.engine.game_map = self.maps[len(self.maps) - 1]

	def descend_floor(self) -> None:
		# Ensure the current map is updated with what has happened
		#self.maps[self.current_floor] = self.engine.game_map
#		print(f"1 Floor: {self.current_floor}, map count: {len(self.maps)}")
		self.current_floor += 1
		if self.current_floor == len(self.maps):
			self.generate_floor()
#		print(f"2 Floor: {self.current_floor}, map count: {len(self.maps)}")
		#self.engine.game_map = self.maps[self.current_floor]
		self.engine.player.x, self.engine.player.y = self.maps[self.current_floor]["stair_up"]
		#self.maps[self.current_floor].entities[0] = self.engine.player

	def ascend_floor(self) -> None:
		if self.current_floor > 0:
		# Ensure the current map is updated with what has happened
			#self.maps[self.current_floor] = self.engine.game_map
			self.current_floor -= 1
		#self.engine.game_map = self.maps[self.current_floor]
		self.engine.player.x, self.engine.player.y = self.maps[self.current_floor]["stair_down"]
		#self.maps[self.current_floor].entities[0] = self.engine.player

	@property
	def items(self) -> Iterator[TItem]:
		yield from (entity for entity in self.maps[self.current_floor]["entities"] if isinstance(entity, TItem))

	def get_blocking_entity_at_location(
		self, location_x: int, location_y: int,
	) -> Optional[TEntity]:
		for entity in self.maps[self.current_floor]["entities"]:
			if (
				entity.blocks_movement
				and entity.x == location_x
				and entity.y == location_y
			):
				return entity
		return None

	def get_actor_at_location(self, x: int, y: int) -> Optional[TActor]:
#		for actor in self.actors:
#			if actor.x == x and actor.y == y:
#				return actor
		return None

	def is_walkable(self, x: int, y: int) -> bool:
		return self.maps[self.current_floor]["tiles"]["walkable"][x, y]

	def in_bounds(self, x: int, y: int) -> bool:
		return 0 <= x < self.maps[self.current_floor]["width"] and 0 <= y < self.maps[self.current_floor]["height"]

	def render(self, console: Console) -> None:
		console.rgb[0 : self.maps[self.current_floor]["width"], 0 : self.maps[self.current_floor]["height"]] = np.select(
			condlist=[self.maps[self.current_floor]["visible"], self.maps[self.current_floor]["explored"]],
			choicelist=[self.maps[self.current_floor]["tiles"]["light"], self.maps[self.current_floor]["tiles"]["dark"]],
			default=tile_types.SHROUD,
		)

		entities_sorted_for_rendering = sorted(
			self.maps[self.current_floor]["entities"], key=lambda x: x.render_order.value
		)

		for entity in entities_sorted_for_rendering:
			if self.maps[self.current_floor]["visible"][entity.x, entity.y]:
				console.print(
					x=entity.x, y=entity.y, string=entity.char, fg=entity.colour
				)
