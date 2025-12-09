from __future__ import annotations
import generator.colours as colour
items: dict = {}

items["food parcel"] = {
	"name": "food parcel",
	"energy": 1000,
	"weight": 1,
	"types": ["pickable", "consumable"],
	"dark": (9576, colour.gray, colour.black),
	"light": (9576, colour.brown, colour.black),
}
items["food dispenser"] = {
	"name": "food dispenser",
	"output": "food parcel",
	"count": 1000,
	"weight": 5000,
	"types": ["static"],
	"dark": (920, colour.gray, colour.black),
	"light": (920, colour.brown, colour.black),
}
items["backpack"] = {
	"name": "backpack",
	"slots": 16,
	"weight": 50,
	"types": ["pickable", "equippable", "container"],
	"equippable": ["back"],
	"dark": (920, colour.gray, colour.black),
	"light": (920, colour.brown, colour.black),
}
items["backpack dispenser"] = {
	"name": "backpack dispenser",
	"output": "backpack",
	"count": 500,
	"weight": 5000,
	"types": ["static"],
	"dark": (920, colour.gray, colour.black),
	"light": (920, colour.brown, colour.black),
}
