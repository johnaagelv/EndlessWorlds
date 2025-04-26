from typing import Tuple
import numpy as np

graphic_dt = np.dtype(
	[
		("ch", np.int32), # Unicode codepoint
		("fg", "3B"), # 3 unsigned bytes, foreground RGB colours
		("bg", "3B"), # Background RGB colours
	]
)

tile_dt = np.dtype(
	[
		("walkable", bool), # True if walkable tile
		("transparent", bool), # True if tile doesn't block FOV
		("dark", graphic_dt), # Graphics outside of FOV
		("light", graphic_dt), # Graphics inside of FOV
		("gateway", bool), # Gateway if true
	]
)

def new_tile(
	*,
	walkable: int,
	transparent: int,
	dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
	light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
	gateway: bool,
) -> np.array:
	return np.array((walkable, transparent, dark, light, gateway), dtype=tile_dt)

tiles = {}

tiles["blank"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord(" "), (0, 0, 0), (0, 0, 0)),
	light=(ord(" "), (0, 0, 0), (0, 0, 0)),
	gateway=False,
)
tiles["floor"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord(" "), (255, 255, 255), (96, 64, 64)),
	light=(ord(" "), (255, 255, 255), (128, 96, 96)),
	gateway=False,
)
tiles["wall"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord("#"), (255, 255, 255), (32, 32, 32)),
	light=(ord("#"), (255, 255, 255), (64, 64, 64)),
	gateway=False,
)
tiles["plain"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord("."), (255, 255, 255), (240, 230, 140)),
	light=(ord("."), (255, 255, 255), (240, 230, 140)),
	gateway=False,
)
