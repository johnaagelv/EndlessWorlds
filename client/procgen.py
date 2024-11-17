import random
from typing import Iterator, Tuple

import tcod

from game_map import TGameMap
import tile_types

class TRoom:
	def __init__(
		self,
		x: int,
		y: int,
		width: int,
		height: int
	):
		self.x1 = x
		self.y1 = y
		self.x2 = x + width
		self.y2 = y + height

	@property
	def center(self) -> Tuple[int, int]:
		center_x = int((self.x1 + self.x2) / 2)
		center_y = int((self.y1 + self.y2) / 2)
		return center_x, center_y

	@property
	def inner(self) -> Tuple[slice, slice]:
		return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

def tunnel_between(
	start: Tuple[int, int],
	end: Tuple[int, int],
) -> Iterator[Tuple[int, int]]:
	x1, y1 = start
	x2, y2 = end
	if random.random() < 0.5:
		corner_x, corner_y = x2, y1
	else:
		corner_x, corner_y = x1, y2
	
	for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
		yield x, y
	for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
		yield x, y

def generate_dungeon(
	map_width,
	map_height,
	player=None
) -> TGameMap:
	dungeon = TGameMap(
		map_width,
		map_height
	)
	room_1 = TRoom(x=10, y=5, width=15, height=25)
	room_2 = TRoom(x=55, y=25, width=10, height=15)

	dungeon.tiles[room_1.inner] = tile_types.floor
	dungeon.tiles[room_2.inner] = tile_types.floor

	for x, y in tunnel_between(room_2.center, room_1.center):
		dungeon.tiles[x, y] = tile_types.floor

	if player:
		player.data["location"]["x"], player.data["location"]["y"] = room_2.center
	return dungeon