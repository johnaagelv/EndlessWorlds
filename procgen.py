from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

import entity_factories
from game_map import GameMap
import tile_types


if TYPE_CHECKING:
	from engine import Engine

# Floor no., Room count, Item count, NPC count, Min size, Max size
build_data = [
	(0, 6, 2, 2, 5, 32),
	(4, 32, 3, 4, 9, 11),
	(7, 8, 5, 4, 5, 9),
]

def get_value_for_floor(floor: int = 0) -> Tuple[int, int, int, int, int, int]:
	current_floor_value = (0, 4, 1, 1, 11, 13)
	for floor_value in build_data:
		if floor_value[0] > floor:
			break
		else:
			current_floor_value = floor_value
	return current_floor_value

class RectangularRoom:
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

	def intersects(self, other: RectangularRoom) -> bool:
		"""Return True if this room overlaps with another RectangularRoom."""
		return (
			self.x1 <= other.x2
			and self.x2 >= other.x1
			and self.y1 <= other.y2
			and self.y2 >= other.y1
		)

def place_entities(
	room: RectangularRoom, dungeon: GameMap, maximum_monsters: int, maximum_items: int
) -> None:
	number_of_monsters = random.randint(0, maximum_monsters)
	number_of_items = random.randint(0, maximum_items)

	for i in range(number_of_monsters):
		x = random.randint(room.x1 + 1, room.x2 - 1)
		y = random.randint(room.y1 + 1, room.y2 - 1)

		if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
			if random.random() < 0.8:
				entity_factories.orc.spawn(dungeon, x, y)
			else:
				entity_factories.troll.spawn(dungeon, x, y)

	for i in range(number_of_items):
		x = random.randint(room.x1 + 1, room.x2 - 1)
		y = random.randint(room.y1 + 1, room.y2 - 1)

		if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
			item_chance = random.random()

			if item_chance < 0.7:
				entity_factories.health_potion.spawn(dungeon, x, y)
			elif item_chance < 0.80:
				entity_factories.fireball_scroll.spawn(dungeon, x, y)
			elif item_chance < 0.90:
				entity_factories.confusion_scroll.spawn(dungeon, x, y)
			else:
				entity_factories.lightning_scroll.spawn(dungeon, x, y)


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
	engine: Engine,
) -> GameMap:
	"""Generate a new dungeon map."""
	# Floor no., Room count, Item count, NPC count, Min size, Max size
	floor_value = get_value_for_floor(engine.game_world.current_floor)
	max_rooms = floor_value[1]
	max_items_per_room = floor_value[2]
	max_monsters_per_room = floor_value[3]
	room_min_size = floor_value[4]
	room_max_size = floor_value[5]
	player = engine.player
	dungeon = GameMap(engine, map_width, map_height, entities=[player])

	rooms: List[RectangularRoom] = []

	center_of_last_room = (0, 0)

	for r in range(max_rooms):
		room_width = random.randint(room_min_size, room_max_size)
		room_height = random.randint(room_min_size, room_max_size)

		x = random.randint(0, dungeon.width - room_width - 1)
		y = random.randint(0, dungeon.height - room_height - 1)

		# "RectangularRoom" class makes rectangles easier to work with
		new_room = RectangularRoom(x, y, room_width, room_height)

		# Run through the other rooms and see if they intersect with this one.
		if any(new_room.intersects(other_room) for other_room in rooms):
			continue  # This room intersects, so go to the next attempt.
		# If there are no intersections then the room is valid.

		# Dig out this rooms inner area.
		dungeon.tiles[new_room.inner] = tile_types.floor

		if len(rooms) == 0:
			# The first room, where the player starts.
			player.place(*new_room.center, dungeon)
			center_of_first_room = new_room.center

		else:  # All rooms after the first.
			# Dig out a tunnel between this room and the previous one.
			for x, y in tunnel_between(rooms[-1].center, new_room.center):
				dungeon.tiles[x, y] = tile_types.floor

			center_of_last_room = new_room.center

			place_entities(new_room, dungeon, max_monsters_per_room, max_items_per_room)

		dungeon.tiles[center_of_last_room] = tile_types.down_stairs
		dungeon.downstairs_location = center_of_last_room

		if engine.game_world.current_floor > 0:
			dungeon.tiles[(center_of_first_room[0]-1, center_of_first_room[1])] = tile_types.up_stairs
			dungeon.upstairs_location = (center_of_first_room[0]-1, center_of_first_room[1])

		# Finally, append the new room to the list.
		rooms.append(new_room)

	return dungeon
