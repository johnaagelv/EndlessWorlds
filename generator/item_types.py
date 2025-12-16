from __future__ import annotations
import numpy as np
from typing import Tuple
import generator.colours as colour

item_dt = np.dtype(
	[
		("face", np.int32), # Face of this item, unicode
		("fg", "4B"), # Foreground colour, RGBA
		("bg", "4B"), # Background colour, RGBA
	]
)

items: dict = {}

def new_item(
	*,
	face: int,
	fg: Tuple[int, int, int, int],
	bg: Tuple[int, int, int, int]
) -> np.ndarray:
	return np.array((face, fg, bg), dtype=item_dt)

item_types: list = [
	"consumables", # food parcel, water, fruit, vegetables, berries, meat, ...
	"wearables", # Boots, helmet, vest, trousers, jacket, hat, armour, gloves, ...
	"weapons", # Gun, rifle, bow, knife, club, staff, sword, taser, ...
	"tools", # Tools - drill, tablet, scanner, medanalyzer, ...
	"operable", # Static machines that can be operated - computer, vending machine, atm, food dispenser, ...
	"moveable", # Moveable machines - car, bicycle, tractor, truck, motorcycle, ...
]

items["food parcel"] = new_item(
	face=9576,
	fg=(255, 255, 255, 255),
	bg=(237, 237, 238, 192)
)
items["backpack"] = new_item(
	face=162,
	fg=colour.food_parcel,
	bg=colour.background
)
