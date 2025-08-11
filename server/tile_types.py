from __future__ import annotations

from typing import Tuple
import numpy as np

import colours

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
) -> np.ndarray:
	return np.array((walkable, transparent, dark, light, gateway), dtype=tile_dt)

# Predefined symbol and colours for out of FOV
floor_dark = (ord(" "), colours.white, colours.black)
# Predefined symbol and colours for inside of FOV 
floor_light = (ord(" "), colours.white, colours.dimgray)
grassland1_dark = (ord("w"), colours.green, colours.sandybrown)
grassland1_light = (ord("w"), colours.lawngreen, colours.sandybrown)
grassland2_dark = (ord("v"), colours.green, colours.sandybrown)
grassland2_light = (ord("v"), colours.lawngreen, colours.sandybrown)

grassland1 = new_tile(
	walkable=True,
	transparent=True,
	dark=grassland1_dark,
	light=grassland1_light,
	gateway=False,
)

grassland2 = new_tile(
	walkable=True,
	transparent=True,
	dark=grassland2_dark,
	light=grassland2_light,
	gateway=False,
)

floor = new_tile(
	walkable=True,
	transparent=True,
	dark=floor_dark,
	light=floor_light,
	gateway=False,
)

wall = new_tile(
	walkable=False,
	transparent=False,
	dark=(43, (255, 255, 255), colours.darkbrown),
	light=(43, (255, 255, 255), colours.darkbrown),
	gateway=False,
)

door_closed = new_tile(
	walkable=False,
	transparent=False,
	dark=(ord("+"), (255, 255, 255), (0, 0, 0)),
	light=(ord("+"), (255, 255, 255), (0, 0, 0)),
	gateway=False,
)

door_open = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord("_"), (255, 255, 255), (0, 0, 0)),
	light=(ord("_"), (255, 255, 255), (0, 0, 0)),
	gateway=True,
)

gate = new_tile(
	walkable=True,
	transparent=False,
	dark=(76, (255, 255, 255), (0, 0, 0)),
	light=(76, (255, 255, 255), (0, 0, 0)),
	gateway=True,
)