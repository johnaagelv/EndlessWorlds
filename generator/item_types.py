from __future__ import annotations
import generator.colours as colour
items: dict = {}

item_types: list = [
	"consumables", # food parcel, water, fruit, vegetables, berries, meat, ...
	"wearables", # Boots, helmet, vest, trousers, jacket, hat, armour, gloves, ...
	"weapons", # Gun, rifle, bow, knife, club, staff, sword, taser, ...
	"tools", # Tools - drill, tablet, scanner, medanalyzer, ...
	"operable", # Static machines that can be operated - computer, vending machine, atm, food dispenser, ...
	"moveable", # Moveable machines - car, bicycle, tractor, truck, motorcycle, ...
]

items["food parcel"] = {
	"name": "food parcel",
	"energy": 1000,
	"weight": 1,
	"types": ["pickable", "consumable"],
	"dark": (9576, colour.spaceship_deck, colour.darkgray),
	"light": (9576, colour.spaceship_deck, colour.lightgray),
}
