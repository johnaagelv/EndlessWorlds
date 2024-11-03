from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
	[
		("ch", np.int32), # Tile unicode
		("fg", "3B"), # Tile foreground RGB
		("bg", "3B"), # Tile background RGB
	]
)

tile_dt = np.dtype(
	[
		("walkable", bool), # Walkable indication
		("transparent", bool),
		("dark", graphic_dt), # Tile graphics when out of FOV
		("light", graphic_dt), # Tile graphics when in FOV
	]
)

def new_tile(
	*,
	walkable: int,
	transparent: int,
	dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
	light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
	return np.array((walkable, transparent, dark, light), dtype=tile_dt)

SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
	light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)

wall = new_tile(
	walkable=False,
	transparent=False,
	dark=(ord(" "), (255, 255, 255), (0, 0, 0)),
	light=(ord(" "), (255, 255, 255), (130, 110, 50)),
)