from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

from entity import TActor, TItem
import tile_types

if TYPE_CHECKING:
	from engine import TEngine
	from entity import TEntity


class TGameMap:
	def __init__(
		self, engine: TEngine, width: int, height: int, entities: Iterable[TEntity] = ()
	):
		self.engine = engine
		self.width, self.height = width, height
		self.entities = list(entities)
		self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

		self.visible = np.full(
			(width, height), fill_value=False, order="F"
		)  # Tiles the player can currently see
		self.explored = np.full(
			(width, height), fill_value=False, order="F"
		)  # Tiles the player has seen before

		self.downstairs_location = (0, 0)
		self.upstairs_location = (0, 0)

	@property
	def gamemap(self) -> TGameMap:
		return self

	@property
	def actors(self) -> Iterator[TActor]:
		"""Iterate over this maps living actors."""
		yield from (
			entity
			for entity in self.entities
			if isinstance(entity, TActor) and entity.is_alive
		)
	
	@property
	def items(self) -> Iterator[TItem]:
		yield from (entity for entity in self.entities if isinstance(entity, TItem))

	def get_blocking_entity_at_location(
		self, location_x: int, location_y: int,
	) -> Optional[TEntity]:
		for entity in self.entities:
			if (
				entity.blocks_movement
				and entity.x == location_x
				and entity.y == location_y
			):
				return entity

		return None

	def get_actor_at_location(self, x: int, y: int) -> Optional[TActor]:
		for actor in self.actors:
			if actor.x == x and actor.y == y:
				return actor

		return None

	def in_bounds(self, x: int, y: int) -> bool:
		"""Return True if x and y are inside of the bounds of this map."""
		return 0 <= x < self.width and 0 <= y < self.height

	def render(self, console: Console) -> None:
		"""
		Renders the map.

		If a tile is in the "visible" array, then draw it with the "light" colors.
		If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
		Otherwise, the default is "SHROUD".
		"""
		console.rgb[0 : self.width, 0 : self.height] = np.select(
			condlist=[self.visible, self.explored],
			choicelist=[self.tiles["light"], self.tiles["dark"]],
			default=tile_types.SHROUD,
		)

		entities_sorted_for_rendering = sorted(
			self.entities, key=lambda x: x.render_order.value
		)

		for entity in entities_sorted_for_rendering:
			if self.visible[entity.x, entity.y]:
				console.print(
					x=entity.x, y=entity.y, string=entity.char, fg=entity.colour
				)

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
	
	def generate_floor(self) -> None:
		from procgen import generate_dungeon
		self.maps.append(
			generate_dungeon(
				map_width = self.map_width,
				map_height = self.map_height,
				engine = self.engine,
			)
		)
		self.engine.game_map = self.maps[len(self.maps) - 1]

	def descend_floor(self) -> None:
		# Ensure the current map is updated with what has happened
		self.maps[self.current_floor] = self.engine.game_map
#		print(f"1 Floor: {self.current_floor}, map count: {len(self.maps)}")
		self.current_floor += 1
		if self.current_floor == len(self.maps):
			self.generate_floor()
#		print(f"2 Floor: {self.current_floor}, map count: {len(self.maps)}")
		self.engine.game_map = self.maps[self.current_floor]
		self.engine.player.x, self.engine.player.y = self.engine.game_map.upstairs_location
		self.engine.game_map.entities[0] = self.engine.player

	def ascend_floor(self) -> None:
		if self.current_floor > 0:
		# Ensure the current map is updated with what has happened
			self.maps[self.current_floor] = self.engine.game_map
			self.current_floor -= 1
		self.engine.game_map = self.maps[self.current_floor]
		self.engine.player.x, self.engine.player.y = self.engine.game_map.downstairs_location
		self.engine.game_map.entities[0] = self.engine.player