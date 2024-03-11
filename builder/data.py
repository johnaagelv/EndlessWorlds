import numpy as np

wall = ord("#") #{"id":0, "face": ord("#"), "desc": "wall"}
floor = ord(".") #{"id": 1, "face": ord("."), "desc": "floor"}

build = {
	"world": {
		"name": "demo",
		"title": "Demo World",
		"maps": ["engine_level"], #, "fuel_level", "cargo_level", "crew_level", "level_1", "level_2", "level_3", "level_4", "command_level"],
	},
	"engine_level": {
		"name": "engine_level",
		"title": "Engine level",
		"width": 41,
		"height": 41,
		"map": [
			# x, y = start position
			# r = radius
			# outer = character to use
			# inner = character to use inside
			{"type": "circle_wall", "x": 19, "y": 19, "r": 19, "t": 3, "outer": "#"}, # Draw spaceship shell
#			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#"}, # Draw lift shell
#			{"type": "entryway", "x": 19, "y": 18, "w": 1, "h": 1, "outer": "+"},
			{"type": "square", "x": 14, "y": 29, "w": 11, "h": 8, "outer": "#", "inner": "."}, # Draw engine block
			{"type": "square", "x": 14, "y": 2, "w": 11, "h": 8, "outer": "#", "inner": "."}, # Draw engine block
			{"type": "square", "x": 2, "y": 14, "w": 8, "h": 11, "outer": "#", "inner": "."}, # Draw engine block
			{"type": "square", "x": 29, "y": 14, "w": 8, "h": 11, "outer": "#", "inner": "."}, # Draw engine block
		]
	},
	"fuel_level": {
		"name": "fuel_level",
		"title": "Fuel level",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle", "x": 19, "y": 19, "r": 19, "outer": "#", "inner": "."},
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#", "inner": "."}
		]
	},
	"cargo_level": {
		"name": "cargo_level",
		"title": "Cargo level",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle", "x": 19, "y": 19, "r": 19, "outer": "#", "inner": "."},
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#", "inner": "."}
		]
	},
	"crew_level": {
		"name": "crew_level",
		"title": "Crew level",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle", "x": 19, "y": 19, "r": 19, "outer": "#", "inner": "."},
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#", "inner": "."}
		]
	},
	"level_1": {
		"name": "level_1",
		"title": "Level 1",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle", "x": 19, "y": 19, "r": 18, "outer": "#", "inner": "."},
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#", "inner": "."}
		]
	},
	"level_2": {
		"name": "level_2",
		"title": "Level 2",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle", "x": 19, "y": 19, "r": 16, "outer": "#", "inner": "."},
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#", "inner": "."}
		]
	},
	"level_3": {
		"name": "level_3",
		"title": "Level 3",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle", "x": 19, "y": 19, "r": 14, "outer": "#", "inner": "."},
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#", "inner": "."}
		]
	},
	"level_4": {
		"name": "level_4",
		"title": "Level 4",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle", "x": 19, "y": 19, "r": 12, "outer": "#", "inner": "."},
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#", "inner": "."}
		]
	},
	"command_level": {
		"name": "command_level",
		"title": "Command level",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle", "x": 19, "y": 19, "r": 10, "outer": "#", "inner": "."},
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#", "inner": "."}
		]
	},
}