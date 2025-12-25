""" Item definitions uses by this client """
from __future__ import annotations
import client.ui.colours as colour

# Item types
item_types: dict = {
	"consumable":	["face", "type", "name", "plural", "adjective", "unique", "weight", "fg", "bg", "energy"], # food parcel, water, fruit, vegetables, berries, meat, ...
	"container":	["face", "type", "name", "plural", "adjective", "unique", "weight", "fg", "bg", "slots"], # backpack, 
	"weapon":		["face", "type", "name", "plural", "adjective", "unique", "weight", "fg", "bg"], # Gun, rifle, bow, knife, club, staff, sword, taser, ...
	"tool":			["face", "type", "name", "plural", "adjective", "unique", "weight", "fg", "bg"], # Tools - drill, tablet, scanner, medanalyzer, ...
	"operable":		["face", "type", "name", "plural", "adjective", "unique", "weight", "fg", "bg"], # Static machines that can be operated - computer, vending machine, atm, food dispenser, ...
	"transport":	["face", "type", "name", "plural", "adjective", "unique", "weight", "fg", "bg"], # car, bicycle, tractor, truck, motorcycle, ...
	"wearables":	["face", "type", "name", "plural", "adjective", "unique", "weight", "fg", "bg"], # Boots, helmet, vest, trousers, jacket, hat, armour, gloves, ...
}

# Item faces and definitions
item_faces: dict = {
	162: {
		"face": 162,
		"type": "container",
		"name": "backpack",
		"plural": "backpacks",
		"adjective": "",
		"unique": True,
		"weight": 2,
		"fg": colour.backpack,
		"bg": colour.background,
		"slots": 10,
	},
	9576: {
		"face": 9576,
		"type": "consumable",
		"name": "food parcel",
		"plural": "food parcels",
		"adjective": "",
		"unique": False,
		"weight": 1,
		"fg": colour.food_parcel,
		"bg": colour.background,
		"energy": 50,
	},
}
