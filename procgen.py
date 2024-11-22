from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

import entity_factories
from game_map import TGameMap
import tile_types


if TYPE_CHECKING:
	from engine import TEngine


class TRectangularRoom:
	def __init__(self, x: int, y: int, width: int, height: int):
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
		"""Return the inner area of this room as a 2D array index."""
		return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

	def intersects(self, other: TRectangularRoom) -> bool:
		"""Return True if this room overlaps with another RectangularRoom."""
		return (
			self.x1 <= other.x2
			and self.x2 >= other.x1
			and self.y1 <= other.y2
			and self.y2 >= other.y1
		)

def place_npcs(
	room: TRectangularRoom, dungeon: TGameMap, maximum_monsters: int
) -> None:
	number_of_monsters = random.randint(0, maximum_monsters)

	for i in range(number_of_monsters):
		x = random.randint(room.x1 + 1, room.x2 - 1)
		y = random.randint(room.y1 + 1, room.y2 - 1)

		if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
			if random.random() < 0.8:
				entity_factories.orc.spawn(dungeon, x, y)
			else:
				entity_factories.troll.spawn(dungeon, x, y)
	
def place_items(
	room: TRectangularRoom, dungeon: TGameMap, maximum_items: int, engine: TEngine
) -> None:
	number_of_items = random.randint(0, maximum_items)

	for i in range(number_of_items):
		x = random.randint(room.x1 + 1, room.x2 - 1)
		y = random.randint(room.y1 + 1, room.y2 - 1)
		if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
			item_chance = random.random()
			if item_chance < 0.7:
				item = entity_factories.health_potion.spawn(dungeon, x, y)
			elif item_chance < 0.8:
				item = entity_factories.fireball_scroll.spawn(dungeon, x, y)
			elif item_chance < 0.9:
				item = entity_factories.confusion_scroll.spawn(dungeon, x, y)
			else:
				item = entity_factories.lightning_scroll.spawn(dungeon, x, y)

			if len(engine.player.inventory.items) < engine.player.inventory.capacity:
				item_chance = random.random()
				if item_chance < 0.5:
					item.parent = engine.player.inventory
					engine.player.inventory.items.append(item)

def tunnel_between(
	start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
	"""Return an L-shaped tunnel between these two points."""
	x1, y1 = start
	x2, y2 = end
	if random.random() < 0.5:  # 50% chance.
		# Move horizontally, then vertically.
		corner_x, corner_y = x2, y1
	else:
		# Move vertically, then horizontally.
		corner_x, corner_y = x1, y2

	# Generate the coordinates for this tunnel.
	for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
		yield x, y
	for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
		yield x, y

def generate_dungeon(
	map_width: int,
	map_height: int,
	engine: TEngine,
) -> TGameMap:
	max_rooms: int = random.randint(1, int(map_width * map_height / 9))
	room_min_size: int = random.randint(3, 6)
	room_max_size: int = random.randint(6, int(map_width / 2))
	max_monsters_per_room: int = random.randint(0, max_rooms // 2)
	max_items_per_room: int = random.randint(0, max_rooms)
	"""Generate a new dungeon map."""
	player = engine.player
	dungeon = TGameMap(engine, map_width, map_height, entities=[player])

	rooms: List[TRectangularRoom] = []

	center_of_last_room = (0, 0)

	for r in range(max_rooms):
		room_width = random.randint(room_min_size, room_max_size)
		room_height = random.randint(room_min_size, room_max_size)

		x = random.randint(0, dungeon.width - room_width - 1)
		y = random.randint(0, dungeon.height - room_height - 1)

		# "RectangularRoom" class makes rectangles easier to work with
		new_room = TRectangularRoom(x, y, room_width, room_height)

		# Run through the other rooms and see if they intersect with this one.
		if any(new_room.intersects(other_room) for other_room in rooms):
			continue  # This room intersects, so go to the next attempt.
		# If there are no intersections then the room is valid.

		# Dig out this rooms inner area.
		dungeon.tiles[new_room.inner] = tile_types.floor

		if len(rooms) == 0:
			# The first room, where the player starts.
			player.place(*new_room.center, dungeon)
			print(f"Floor: {engine.game_world.current_floor} at {new_room.center!r}")
			if engine.game_world.current_floor > 0:
				dungeon.tiles[(player.x - 1, player.y)] = tile_types.stairs_up
				dungeon.upstairs_location = (player.x - 1, player.y)

		else:  # All rooms after the first.
			# Dig out a tunnel between this room and the previous one.
			for x, y in tunnel_between(rooms[-1].center, new_room.center):
				dungeon.tiles[x, y] = tile_types.floor
			
			center_of_last_room = new_room.center

			place_npcs(new_room, dungeon, max_monsters_per_room)
			place_items(new_room, dungeon, max_items_per_room, engine)

		center_of_last_room = (player.x + 1, player.y)
		dungeon.tiles[center_of_last_room] = tile_types.stairs_down
		dungeon.downstairs_location = center_of_last_room

		# Finally, append the new room to the list.
		rooms.append(new_room)

	return dungeon
