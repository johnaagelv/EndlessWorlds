from typing import Tuple
import numpy as np

import colours as colour

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

tiles = {}

tiles["blank"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord(" "), colour.black, colour.black),
	light=(ord(" "), colour.black, colour.black),
	gateway=False,
)
tiles["floor"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(32, colour.silver, colour.black),
	light=(32, colour.white, colour.black),
	gateway=False,
)
tiles["wall"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(43, colour.silver, (32, 32, 32)),
	light=(43, colour.white, (64, 64, 64)),
	gateway=False,
)
tiles["gate"] = new_tile(
	walkable=True,
	transparent=False,
	dark=(19, (160, 160, 160), (0, 0, 0)),
	light=(19, (192, 192, 192), (0, 0, 0)),
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
tiles["stairway_down"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(62, (192, 192, 192), (0, 0, 0)),
	light=(62, (255, 255, 255), (0, 0, 0)),
	gateway=False,
)
tiles["stairway_up"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(60, (192, 192, 192), (0, 0, 0)),
	light=(60, (255, 255, 255), (0, 0, 0)),
	gateway=False,
)
tiles["stairway"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord('X'), (192, 192, 192), (0, 0, 0)),
	light=(ord('X'), (255, 255, 255), (0, 0, 0)),
	gateway=False,
)
tiles["grass1"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(44, (128, 192, 128), (0, 0, 0)),
	light=(44, (128, 255, 128), (0, 0, 0)),
	gateway=False,
)
tiles["grass2"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(46, (96, 128, 96), (0, 0, 0)),
	light=(46, (128, 192, 128), (0, 0, 0)),
	gateway=False,
)
tiles["rock1"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(ord("#"), (80, 80, 80), (80, 80, 80)),
	light=(ord("#"), (80, 80, 80), (80, 80, 80)),
	gateway=False,
)
tiles["rock2"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(ord("#"), (64, 64, 64), (64, 64, 64)),
	light=(ord("#"), (64, 64, 64), (64, 64, 64)),
	gateway=False,
)
tiles["underground"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(32, (32, 32, 32), (32, 32, 32)),
	light=(32, (48, 48, 48), (48, 48, 48)),
	gateway=False,
)
tiles["space"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord(" "), (0, 0, 0), (0, 0, 0)),
	light=(ord(" "), (0, 0, 0), (0, 0, 0)),
	gateway=False,
)
tiles["space with small star"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(183, (128, 128, 128), (0, 0, 0)),
	light=(183, (128, 128, 128), (0, 0, 0)),
	gateway=False,
)
tiles["space with star"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(183, colour.silver, colour.black),
	light=(183, colour.silver, colour.black),
	gateway=False,
)
tiles["spaceship deck"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(32, colour.spaceship_deck, colour.spaceship_deck),
	light=(32, colour.spaceship_deck, colour.spaceship_deck),
	gateway=False,
)
tiles["spaceship shell"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9608, colour.spaceship_shell, colour.spaceship_shell),
	light=(9608, colour.spaceship_shell, colour.spaceship_shell),
	gateway=False,
)
tiles["spaceship wall"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9608, colour.spaceship_wall, colour.spaceship_wall),
	light=(9608, colour.spaceship_wall, colour.spaceship_wall),
	gateway=False,
)
tiles["spaceship console"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(242, colour.white, colour.spaceship_deck),
	light=(243, colour.white, colour.spaceship_deck),
	gateway=False,
)
tiles["spaceship lift"] = new_tile(
	walkable=True,
	transparent=False,
	dark=(9578, colour.black, colour.spaceship_deck),
	light=(9579, colour.silver, colour.spaceship_deck),
	gateway=False,
)
tiles["spaceship stairs"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(88, colour.darkgray, colour.spaceship_deck),
	light=(88, colour.darkgray, colour.spaceship_deck),
	gateway=False,
)
tiles["popsicle"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9786, colour.cryo_fluid, colour.cryo_base),
	light=(9786, colour.cryo_fluid, colour.cryo_base),
	gateway=False,
)
tiles["spaceship safety door"] = new_tile(
	walkable=True,
	transparent=False,
	dark=(9532, colour.yellow_safety, colour.spaceship_wall),
	light=(9532, colour.yellow_safety, colour.spaceship_wall),
	gateway=False,
)
tiles["spaceship cabin door"] = new_tile(
	walkable=True,
	transparent=False,
	dark=(9532, colour.darkgray, colour.spaceship_wall),
	light=(9532, colour.darkgray, colour.spaceship_wall),
	gateway=False,
)
tiles["spaceship container"] = new_tile(
	walkable=True,
	transparent=False,
	dark=(9532, colour.spaceship_container, colour.spaceship_wall),
	light=(9532, colour.spaceship_container, colour.spaceship_wall),
	gateway=False,
)
tiles["cryopipe upper left"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9554, colour.cryo_fluid, colour.spaceship_wall),
	light=(9554, colour.cryo_fluid, colour.spaceship_wall),
	gateway=False,
)
tiles["cryopipe horizontal"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9472, colour.cryo_fluid, colour.spaceship_wall),
	light=(9472, colour.cryo_fluid, colour.spaceship_wall),
	gateway=False,
)
tiles["cryopipe cross"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9568, colour.cryo_fluid, colour.spaceship_wall),
	light=(9568, colour.cryo_fluid, colour.spaceship_wall),
	gateway=False,
)
tiles["cryopipe upper t"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9516, colour.cryo_fluid, colour.spaceship_wall),
	light=(9516, colour.cryo_fluid, colour.spaceship_wall),
	gateway=False,
)
tiles["cryopipe left t"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9500, colour.cryo_fluid, colour.spaceship_wall),
	light=(9500, colour.cryo_fluid, colour.spaceship_wall),
	gateway=False,
)
tiles["cryopipe right t"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9508, colour.cryo_fluid, colour.spaceship_wall),
	light=(9508, colour.cryo_fluid, colour.spaceship_wall),
	gateway=False,
)
tiles["cryopipe upper right"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9558, colour.cryo_fluid, colour.spaceship_wall),
	light=(9558, colour.cryo_fluid, colour.spaceship_wall),
	gateway=False,
)
tiles["cryopipe vertical"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9474, colour.cryo_fluid, colour.spaceship_wall),
	light=(9474, colour.cryo_fluid, colour.spaceship_wall),
	gateway=False,
)
tiles["cryopipe lower right"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9496, colour.cryo_fluid, colour.spaceship_wall),
	light=(9496, colour.cryo_fluid, colour.spaceship_wall),
	gateway=False,
)
tiles["cryopipe lower left"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9492, colour.cryo_fluid, colour.spaceship_wall),
	light=(9492, colour.cryo_fluid, colour.spaceship_wall),
	gateway=False,
)
tiles["cryotank"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9608, colour.cryo_base, colour.cryo_fluid),
	light=(9608, colour.cryo_base, colour.cryo_fluid),
	gateway=False,
)
tiles["spaceship propulsion"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9688, colour.silver, colour.black),
	light=(9688, colour.silver, colour.yellow),
	gateway=False,
)
tiles["propulsion fluid"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(35, colour.space_cadet, colour.goldenrod),
	light=(9618, colour.space_cadet, colour.goldenrod),
	gateway=False,
)
