from __future__ import annotations

from typing import Tuple
import generator.colours as colour

items: dict = {}

def new_item(
	name: str,
	face: int,
	fg: Tuple[int, int, int, int],
	bg: Tuple[int, int, int, int],
) -> dict:
	return {"name": name, "face": face, "fg": fg, "bg": bg}

item_types: list = [
	"consumables", # food parcel, water, fruit, vegetables, berries, meat, ...
	"wearables", # Boots, helmet, vest, trousers, jacket, hat, armour, gloves, ...
	"weapons", # Gun, rifle, bow, knife, club, staff, sword, taser, ...
	"tools", # Tools - drill, tablet, scanner, medanalyzer, ...
	"operable", # Static machines that can be operated - computer, vending machine, atm, food dispenser, ...
	"moveable", # Moveable machines - car, bicycle, tractor, truck, motorcycle, ...
]

items["food parcel"] = new_item(
	"Food parcel",
	9576,
	colour.food_parcel,
	colour.background,
)
items["backpack"] = new_item(
	"Backpack",
	162,
	colour.backpack,
	colour.background,
)
