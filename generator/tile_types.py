from __future__ import annotations

from typing import Tuple
import numpy as np

import generator.colours as colour

graphic_dt = np.dtype(
	[
		("ch", np.int32), # Unicode codepoint
		("fg", "4B"), # 3 unsigned bytes, foreground RGB colours
		("bg", "4B"), # Background RGB colours
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
	dark: Tuple[int, Tuple[int, int, int, int], Tuple[int, int, int, int]],
	light: Tuple[int, Tuple[int, int, int, int], Tuple[int, int, int, int]],
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
	dark=(43, colour.silver, (32, 32, 32, 255)),
	light=(43, colour.white, (64, 64, 64, 255)),
	gateway=False,
)
tiles["gate"] = new_tile(
	walkable=True,
	transparent=False,
	dark=(19, (160, 160, 160, 255), (0, 0, 0, 255)),
	light=(19, (192, 192, 192, 255), (0, 0, 0, 255)),
	gateway=False,
)
tiles["plain"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord("."), (128, 192, 128, 255), (0, 0, 0, 255)),
	light=(ord("."), (128, 255, 128, 255), (0, 0, 0, 255)),
	gateway=False,
)
tiles["gateway"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(76, (192, 192, 192, 255), (0, 0, 0, 255)),
	light=(77, (255, 255, 255, 255), (0, 0, 0, 255)),
	gateway=True,
)
tiles["stairway down"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(62, (192, 192, 192, 255), (0, 0, 0, 255)),
	light=(62, (255, 255, 255, 255), (0, 0, 0, 255)),
	gateway=True,
)
tiles["stairway up"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(60, (192, 192, 192, 255), (0, 0, 0, 255)),
	light=(60, (255, 255, 255, 255), (0, 0, 0, 255)),
	gateway=True,
)
tiles["stairway"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord('X'), (192, 192, 192, 255), (0, 0, 0, 255)),
	light=(ord('X'), (255, 255, 255, 255), (0, 0, 0, 255)),
	gateway=True,
)
tiles["coastline1"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(44, colour.black, colour.coastline1),
	light=(44, colour.black, colour.coastline2),
	gateway=False,
)
tiles["coastline2"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(46, colour.black, colour.coastline2),
	light=(46, colour.black, colour.coastline3),
	gateway=False,
)
tiles["coastline3"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(39, colour.black, colour.coastline3),
	light=(39, colour.black, colour.coastline1),
	gateway=False,
)
tiles["ocean1"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(124, colour.black, colour.ocean1),
	light=(124, colour.black, colour.ocean2),
	gateway=False,
)
tiles["ocean2"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(163, colour.black, colour.ocean2),
	light=(163, colour.black, colour.ocean3),
	gateway=False,
)
tiles["ocean3"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(124, colour.black, colour.ocean3),
	light=(124, colour.black, colour.ocean4),
	gateway=False,
)
tiles["ocean4"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(163, colour.black, colour.ocean4),
	light=(163, colour.black, colour.ocean5),
	gateway=False,
)
tiles["ocean5"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(124, colour.black, colour.ocean5),
	light=(124, colour.black, colour.ocean6),
	gateway=False,
)
tiles["ocean6"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(163, colour.black, colour.ocean6),
	light=(163, colour.black, colour.ocean1),
	gateway=False,
)
tiles["grass1"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(44, colour.grass1, colour.grass_background),
	light=(44, colour.grass1, colour.grass_background),
	gateway=False,
)
tiles["grass2"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(46, colour.grass2, colour.grass_background),
	light=(46, colour.grass2, colour.grass_background),
	gateway=False,
)
tiles["grass3"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(35, colour.grass3, colour.grass_background),
	light=(35, colour.grass3, colour.grass_background),
	gateway=False,
)
tiles["grass4"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(44, colour.grass4, colour.grass_background),
	light=(44, colour.grass4, colour.grass_background),
	gateway=False,
)
tiles["grass5"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(46, colour.grass5, colour.grass_background),
	light=(46, colour.grass5, colour.grass_background),
	gateway=False,
)
tiles["grass6"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(35, colour.grass6, colour.grass_background),
	light=(35, colour.grass6, colour.grass_background),
	gateway=False,
)
tiles["rock1"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(ord("#"), (80, 80, 80, 255), (80, 80, 80, 255)),
	light=(ord("#"), (80, 80, 80, 255), (80, 80, 80, 255)),
	gateway=False,
)
tiles["rock2"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(ord("#"), (64, 64, 64, 255), (64, 64, 64, 255)),
	light=(ord("#"), (64, 64, 64, 255), (64, 64, 64, 255)),
	gateway=False,
)
tiles["underground"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(37, colour.saddlebrown2, colour.black),
	light=(39, colour.saddlebrown2, colour.black),
	gateway=False,
)
tiles["underground2"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(39, colour.saddlebrown, colour.black),
	light=(37, colour.saddlebrown, colour.black),
	gateway=False,
)
tiles["space"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord(" "), (0, 0, 0, 255), (0, 0, 0, 255)),
	light=(ord(" "), (0, 0, 0, 255), (0, 0, 0, 255)),
	gateway=False,
)
tiles["space with small star"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(183, (128, 128, 128, 255), (0, 0, 0, 255)),
	light=(183, (128, 128, 128, 255), (0, 0, 0, 255)),
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
	dark=(9617, colour.spaceship_deck, colour.darkgray),
	light=(9617, colour.spaceship_deck, colour.lightgray),
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
	gateway=True,
)
tiles["popsicle"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9608, colour.darkslategray, colour.cryo_base),
	light=(9608, colour.darkslategray, colour.cryo_base),
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
	dark=(9554, colour.cryo_fluid, colour.cryo_base),
	light=(9554, colour.cryo_fluid, colour.cryo_base),
	gateway=False,
)
tiles["cryopipe horizontal"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9472, colour.cryo_fluid, colour.cryo_base),
	light=(9472, colour.cryo_fluid, colour.cryo_base),
	gateway=False,
)
tiles["cryopipe cross"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9568, colour.cryo_fluid, colour.cryo_base),
	light=(9568, colour.cryo_fluid, colour.cryo_base),
	gateway=False,
)
tiles["cryopipe upper t"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9516, colour.cryo_fluid, colour.cryo_base),
	light=(9516, colour.cryo_fluid, colour.cryo_base),
	gateway=False,
)
tiles["cryopipe left t"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9500, colour.cryo_fluid, colour.cryo_base),
	light=(9500, colour.cryo_fluid, colour.cryo_base),
	gateway=False,
)
tiles["cryopipe right t"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9508, colour.cryo_fluid, colour.cryo_base),
	light=(9508, colour.cryo_fluid, colour.cryo_base),
	gateway=False,
)
tiles["cryopipe upper right"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9558, colour.cryo_fluid, colour.cryo_base),
	light=(9558, colour.cryo_fluid, colour.cryo_base),
	gateway=False,
)
tiles["cryopipe vertical"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9474, colour.cryo_fluid, colour.cryo_base),
	light=(9474, colour.cryo_fluid, colour.cryo_base),
	gateway=False,
)
tiles["cryopipe lower right"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9496, colour.cryo_fluid, colour.cryo_base),
	light=(9496, colour.cryo_fluid, colour.cryo_base),
	gateway=False,
)
tiles["cryopipe lower left"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9492, colour.cryo_fluid, colour.cryo_base),
	light=(9492, colour.cryo_fluid, colour.cryo_base),
	gateway=False,
)
tiles["cryotank"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9608, colour.cryo_fluid, colour.cryo_base),
	light=(9608, colour.cryo_fluid, colour.cryo_base),
	gateway=False,
)
tiles["cryocontainer"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9688, colour.cryo_fluid, colour.cryo_base),
	light=(9688, colour.cryo_fluid, colour.cryo_base),
	gateway=False,
)
tiles["spaceship propulsion"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(9688, colour.darkslateblue, colour.goldenrod),
	light=(9688, colour.darkslateblue, colour.goldenrod),
	gateway=False,
)
tiles["propulsion fluid"] = new_tile(
	walkable=False,
	transparent=False,
	dark=(35, colour.space_cadet, colour.goldenrod),
	light=(9618, colour.space_cadet, colour.goldenrod),
	gateway=False,
)
tiles["matter transporter"] = new_tile(
	walkable=True,
	transparent=False,
	dark=(162, colour.gray, colour.black),
	light=(162, colour.gray, colour.black),
	gateway=True,
)
tiles["spaceship glass wall right"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(9616, colour.glass_wall, colour.spaceship_deck),
	light=(9616, colour.glass_wall, colour.spaceship_deck),
	gateway=False,
)
tiles["ocean coastline"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(163, colour.mediumblue, colour.darkblue),
	light=(163, colour.mediumblue, colour.darkblue),
	gateway=False,
)
tiles["ocean deep"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(163, colour.darkblue, colour.darkblue),
	light=(163, colour.darkblue, colour.darkblue),
	gateway=False,
)

# ISLAND
tiles["DEEPWATER"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(ord("~"),(0, 62, 178, 255), (0, 62, 178, 192)),
	light=(ord("~"),(0, 62, 178, 255), (0, 62, 178, 192)),
	gateway=False,
)
tiles["WATER"] = new_tile(
	walkable=False,
	transparent=True,
	dark=(ord("~"),(9, 82, 198, 255), (9, 82, 198, 192)),
	light=(ord("~"),(9, 82, 198, 255), (9, 82, 198, 192)),
	gateway=False
)
tiles["SAND"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(44,(254, 224, 179, 255), (254, 224, 179, 192)),
	light=(44,(254, 224, 179, 255), (254, 224, 179, 192)),
	gateway=False
)
tiles["GRASS"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(44,(9, 120, 93, 255), (9, 120, 93, 192)),
	light=(44,(9, 120, 93, 255), (9, 120, 93, 192)),
	gateway=False
)
tiles["DARKGRASS"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(44,(10, 107, 72, 255), (10, 107, 72, 192)),
	light=(44,(10, 107, 72, 255), (10, 107, 72, 192)),
	gateway=False
)
tiles["DARKESTGRASS"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(44,(11, 94, 51, 255), (11, 94, 51, 192)),
	light=(44,(11, 94, 51, 255), (11, 94, 51, 192)),
	gateway=False
)
tiles["DARKROCKS"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(44,(140, 142, 123, 255), (140, 142, 123, 192)),
	light=(44,(140, 142, 123, 255), (140, 142, 123, 192)),
	gateway=False
)
tiles["ROCKS"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(44,(160, 162, 143, 255), (160, 162, 143, 192)),
	light=(44,(160, 162, 143, 255), (160, 162, 143, 192)),
	gateway=False
)
tiles["SNOW"] = new_tile(
	walkable=True,
	transparent=True,
	dark=(44,(255, 255, 255, 255), (255, 255, 255, 192)),
	light=(44,(255, 255, 255, 255), (255, 255, 255, 192)),
	gateway=False
)
