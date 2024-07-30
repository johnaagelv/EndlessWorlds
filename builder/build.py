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
	"name": "world"
}