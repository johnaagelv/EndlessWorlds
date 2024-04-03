import numpy as np

tiles = {
	"#": {"name": "wall", "walkable": False, "transparent": False},
	" ": {"name": "deck", "walkable": True, "transparent": True},
	".": {"name": "deck", "walkable": True, "transparent": True},
	"H": {"name": "monitor", "walkable": False, "transparent": False},
	"+": {"name": "entryway", "walkable": False, "transparent": False, "action": {"type": "slide", "swap": ["walkable", "transparent"] } },
	"O": {"name": "wall", "walkable": False, "transparent": False},
	"x": {"name": "stairway", "walkable": True, "transparent": True, "action": {"type": "level", "move": [">","<"] } },
	"~": {"name": "fuel", "walkable": True, "transparent": False},
}
wall = ord("#") #{"id":0, "face": ord("#"), "desc": "wall"}
floor = ord(".") #{"id": 1, "face": ord("."), "desc": "floor"}

build = {
	"world": {
		"name": "demo",
		"title": "Surveyor I",
		"maps": [
#			"engine_level",
			"fuel_level",
#			"cargo_level",
#			"crew_level",
#			"level_1",
#			"level_2",
#			"level_3",
#			"level_4",
#			"command_level"
		],
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
			{"type": "circle", "x": 19, "y": 19, "r": 19, "t": 2, "outer": "#"}, # Draw spaceship shell
			{"type": "square", "x": 18, "y": 18, "w": 3, "h": 3, "outer": "#", "inner": "."}, # Draw lift shell
			{"type": "entryway", "x": 19, "y": 18, "w": 1, "h": 1, "outer": "+"},
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
			{"type": "circle", "x": 19, "y": 19, "r": 19, "t": 2, "outer": "#"}, # Draw spaceship shell
			{"type": "circle", "x": 19, "y": 9, "r": 7, "t": 1, "outer": "O", "inner": "~"}, # Draw fuel tank
			{"type": "circle", "x": 19, "y": 29, "r": 7, "t": 1, "outer": "O"}, # Draw fuel tank
			{"type": "circle", "x": 9, "y": 19, "r": 7, "t": 1, "outer": "O"}, # Draw fuel tank
			{"type": "circle", "x": 29, "y": 19, "r": 7, "t": 1, "outer": "O"}, # Draw fuel tank
			{"type": "square", "x": 18, "y": 18, "w": 3, "h": 3, "outer": "#"}, # Draw lift shell
			{"type": "accessway", "x": 19, "y": 18, "outer": "+", "actions": [
				{"action": "open", "key": "o", "swap": ["walkable", "transparent"]},
			]},
			{"type": "accessway", "x": 19, "y": 19, "outer": "_", "actions": [
				{"action": "level", "key": "?", "choice": ["engine_level", "cargo_level", "crew_level", "level_1", "level_2", "level_3", "level_4", "command_level"]},
			]},
			{"type": "square", "x": 18, "y": 22, "w": 3, "h": 1, "outer": "#"}, # Draw stairway shell
			{"type": "square", "x": 18, "y": 21, "w": 3, "h": 1, "outer": "."}, 
			{"type": "accessway", "x": 19, "y": 21, "outer": "x", "actions": [
				{"action": "down", "key": ">", "level": "engine_level"},
				{"action": "up", "key": "<", "level": "cargo_level"},
			]},
			{"type": "square", "x": 8, "y": 6, "w": 5, "h": 6, "outer": "#", "inner": "."}, # Draw fuel control center
			{"type": "accessway", "x": 10, "y": 11, "outer": "+", "actions": [
				{"action": "open", "key": "o", "swap": ["walkable", "transparent"]},
			]},
			{"type": "square", "x": 11, "y": 7, "w": 1, "h": 4, "outer": "H"},
		]
	},
	"cargo_level": {
		"name": "cargo_level",
		"title": "Cargo level",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle_wall", "x": 19, "y": 19, "r": 19, "t": 2, "outer": "#"}, # Draw spaceship shell
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 18, "w": 3, "h": 3, "outer": "#", "inner": "."}, # Draw lift shell
			{"type": "entryway", "x": 19, "y": 18, "w": 1, "h": 1, "outer": "+"},
			{"type": "square", "x": 18, "y": 20, "w": 3, "h": 3, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 22, "w": 3, "h": 1, "outer": "."}, 
			{"type": "square", "x": 19, "y": 22, "w": 1, "h": 1, "outer": "x"}, # Stairway up/down
		]
	},
	"crew_level": {
		"name": "crew_level",
		"title": "Crew level",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle_wall", "x": 19, "y": 19, "r": 19, "t": 2, "outer": "#"}, # Draw spaceship shell
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 18, "w": 3, "h": 3, "outer": "#", "inner": "."}, # Draw lift shell
			{"type": "entryway", "x": 19, "y": 18, "w": 1, "h": 1, "outer": "+"},
			{"type": "square", "x": 18, "y": 20, "w": 3, "h": 3, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 22, "w": 3, "h": 1, "outer": "."}, 
			{"type": "square", "x": 19, "y": 22, "w": 1, "h": 1, "outer": "x"}, # Stairway up/down
		]
	},
	"level_1": {
		"name": "level_1",
		"title": "Level 1",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle_wall", "x": 19, "y": 19, "r": 19, "t": 2, "outer": "#"}, # Draw spaceship shell
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 18, "w": 3, "h": 3, "outer": "#", "inner": "."}, # Draw lift shell
			{"type": "entryway", "x": 19, "y": 18, "w": 1, "h": 1, "outer": "+"},
			{"type": "square", "x": 18, "y": 20, "w": 3, "h": 3, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 22, "w": 3, "h": 1, "outer": "."}, 
			{"type": "square", "x": 19, "y": 22, "w": 1, "h": 1, "outer": "x"}, # Stairway up/down
		]
	},
	"level_2": {
		"name": "level_2",
		"title": "Level 2",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle_wall", "x": 19, "y": 19, "r": 16, "t": 2, "outer": "#"}, # Draw spaceship shell
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 18, "w": 3, "h": 3, "outer": "#", "inner": "."}, # Draw lift shell
			{"type": "entryway", "x": 19, "y": 18, "w": 1, "h": 1, "outer": "+"},
			{"type": "square", "x": 18, "y": 20, "w": 3, "h": 3, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 22, "w": 3, "h": 1, "outer": "."}, 
			{"type": "square", "x": 19, "y": 22, "w": 1, "h": 1, "outer": "x"}, # Stairway up/down
		]
	},
	"level_3": {
		"name": "level_3",
		"title": "Level 3",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle_wall", "x": 19, "y": 19, "r": 14, "t": 2, "outer": "#"}, # Draw spaceship shell
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 18, "w": 3, "h": 3, "outer": "#", "inner": "."}, # Draw lift shell
			{"type": "entryway", "x": 19, "y": 18, "w": 1, "h": 1, "outer": "+"},
			{"type": "square", "x": 18, "y": 20, "w": 3, "h": 3, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 22, "w": 3, "h": 1, "outer": "."}, 
			{"type": "square", "x": 19, "y": 22, "w": 1, "h": 1, "outer": "x"}, # Stairway up/down
		]
	},
	"level_4": {
		"name": "level_4",
		"title": "Level 4",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle_wall", "x": 19, "y": 19, "r": 12, "t": 2, "outer": "#"}, # Draw spaceship shell
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 18, "w": 3, "h": 3, "outer": "#", "inner": "."}, # Draw lift shell
			{"type": "entryway", "x": 19, "y": 18, "w": 1, "h": 1, "outer": "+"},
			{"type": "square", "x": 18, "y": 20, "w": 3, "h": 3, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 22, "w": 3, "h": 1, "outer": "."}, 
			{"type": "square", "x": 19, "y": 22, "w": 1, "h": 1, "outer": "x"}, # Stairway up/down
		]
	},
	"command_level": {
		"name": "command_level",
		"title": "Command level",
		"width": 41,
		"height": 41,
		"map": [
			{"type": "circle_wall", "x": 19, "y": 19, "r": 10, "t": 2, "outer": "#"}, # Draw spaceship shell
			{"type": "circle", "x": 19, "y": 19, "r": 2, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 18, "w": 3, "h": 3, "outer": "#", "inner": "."}, # Draw lift shell
			{"type": "entryway", "x": 19, "y": 18, "w": 1, "h": 1, "outer": "+"},
			{"type": "square", "x": 18, "y": 20, "w": 3, "h": 3, "outer": "#"}, # Draw lift shell
			{"type": "square", "x": 18, "y": 22, "w": 3, "h": 2, "outer": "."}, 
			{"type": "square", "x": 18, "y": 22, "w": 1, "h": 1, "outer": "x"}, # Stairway up/down
		]
	},
}