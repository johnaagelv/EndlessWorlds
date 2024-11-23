from typing import Tuple

import numpy as np  # type: ignore

import colours as colour

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

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), colour.floor_dark, colour.floor_dark),
    light=(ord(" "), colour.floor_light, colour.floor_light),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("#"), colour.black, colour.wall_dark),
    light=(ord("#"), colour.black, colour.wall_light),
)
stairs_down = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), colour.black, colour.floor_dark),
    light=(ord(">"), colour.black, colour.floor_light),
)

stairs_up = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("<"), colour.black, colour.floor_dark),
    light=(ord("<"), colour.black, colour.floor_light),
)
