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
	dark=(ord("."), (192, 192, 192), (0, 0, 0)),
	light=(ord("."), (255, 255, 255), (0, 0, 0)),
	gateway=False,
)
tiles["wall"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(32, (192, 192, 192), (32, 32, 32)),
	light=(32, (255, 255, 255), (64, 64, 64)),
	gateway=False,
)
tiles["plain"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord("."), (128, 192, 128), (0, 0, 0)),
	light=(ord("."), (128, 255, 128), (0, 0, 0)),
	gateway=False,
)
tiles["gateway"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(76, (192, 192, 192), (0, 0, 0)),
	light=(77, (255, 255, 255), (0, 0, 0)),
	gateway=True,
)
tiles["downstair"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(46, (192, 192, 192), (0, 0, 0)),
	light=(76, (255, 255, 255), (0, 0, 0)),
	gateway=False,
)
tiles["upstair"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(44, (192, 192, 192), (0, 0, 0)),
	light=(44, (255, 255, 255), (0, 0, 0)),
	gateway=False,
)
