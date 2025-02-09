from typing import Tuple

from tcod import tileset
import numpy as np  # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
	[
		("ch", np.int32),  # Unicode codepoint.
		("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
		("bg", "3B"),
	]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
	[
		("walkable", bool),  # True if this tile can be walked over.
		("transparent", bool),  # True if this tile doesn't block FOV.
		("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
		("light", graphic_dt),  # Graphics for when the tile is in FOV.
	]
)


def new_tile(
	*,  # Enforce the use of keywords, so that parameter order doesn't matter.
	walkable: int,
	transparent: int,
	dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
	light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
	"""Helper function for defining individual tile types """
	return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floors = [
	new_tile(
		walkable=True,
		transparent=True,
		dark=(tileset.CHARMAP_CP437[96], (48, 48, 48), (96, 96, 96)),
		light=(tileset.CHARMAP_CP437[96], (80, 80, 80), (128, 128, 128)),
	),
	new_tile(
		walkable=True,
		transparent=True,
		dark=(tileset.CHARMAP_CP437[96], (64, 64, 64), (96, 96, 96)),
		light=(tileset.CHARMAP_CP437[96], (96, 96, 96), (128, 128, 128)),
	),
	new_tile(
		walkable=True,
		transparent=True,
		dark=(tileset.CHARMAP_CP437[96], (32, 32, 32), (96, 96, 96)),
		light=(tileset.CHARMAP_CP437[96], (64, 64, 64), (128, 128, 128)),
	),
]
walls = [
	new_tile(
		walkable=False,
		transparent=False,
		dark=(tileset.CHARMAP_CP437[61], (139-8, 69-8, 19-8), (139-16, 69-16, 19-16)),
		light=(tileset.CHARMAP_CP437[61], (139, 69, 19), (139+96, 69+96, 19+96)),
	),
	new_tile(
		walkable=False,
		transparent=False,
		dark=(tileset.CHARMAP_CP437[61], (139, 69, 19), (139-8, 69-8, 19-8)),
		light=(tileset.CHARMAP_CP437[61], (139, 69, 19), (139+64, 69+64, 19+64)),
	),
	new_tile(
		walkable=False,
		transparent=False,
		dark=(tileset.CHARMAP_CP437[61], (139-32, 69, 19), (139-16, 69-16, 19-16)),
		light=(tileset.CHARMAP_CP437[61], (139, 69, 19), (139+32, 69+32, 19+32)),
	),
]
floor = new_tile(
	walkable=True,
	transparent=True,
	dark=(tileset.CHARMAP_CP437[178], (64, 64, 64), (96, 96, 96)),
	light=(tileset.CHARMAP_CP437[177], (96, 96, 96), (128, 128, 128)),
)
wall = new_tile(
	walkable=False,
	transparent=False,
	dark=(tileset.CHARMAP_CP437[43], (96, 96, 96), (96, 96, 96)),
	light=(tileset.CHARMAP_CP437[43], (128, 128, 128), (128, 128, 128)),
)
down_stairs = new_tile(
	walkable=True,
	transparent=True,
	dark=(tileset.CHARMAP_CP437[ord(">")], (192, 192, 192), (32, 32, 32)),
	light=(tileset.CHARMAP_CP437[ord(">")], (255, 255, 255), (64, 64, 64)),
)

up_stairs = new_tile(
	walkable=True,
	transparent=True,
	dark=(tileset.CHARMAP_CP437[ord("<")], (192, 192, 192), (32, 32, 32)),
	light=(tileset.CHARMAP_CP437[ord("<")], (255, 255, 255), (64, 64, 64)),
)
