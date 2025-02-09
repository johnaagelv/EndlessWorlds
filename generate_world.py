from typing import Tuple
import numpy as np  # type: ignore
from tile_types import new_tile

black = Tuple(0,0,0)

# Walkable, Transparent, Destructable, Harvestable, Foreground colour, Background color
tiles = [
	(False, True, False, False, (0x0000, 0x0000, 0x0000), (0x0000, 0x0000, 0x0000)), # empty space
	(False, False, False, False, (0, 0, 0), (0, 0, 0)), # rock
	(True, True, False, False, (0, 0, 0), (0, 0, 0)), # plain
	(True, True, False, False, (0, 0, 0), (0, 0, 0)), # forest
	(True, True, False, False, (0, 0, 0), (0, 0, 0)), # scrubland

	(False, False, False, True, (0, 0, 0), (0, 0, 0)), # Gold ore
	(False, False, False, True, (0, 0, 0), (0, 0, 0)), # Silver ore
	(False, False, False, True, (0, 0, 0), (0, 0, 0)), # Coal ore
]

tile_names = [
	"empty space",
	"rock",
	"plain",
	"forest",
	"scrub",
	"gold ore",
	"silver ore",
	"coal ore",
	""
]

world = {
	"maps": [
		{
			"name": "Starship Surveyor I",
			"width": 10,
			"height": 10,
			"map": [
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		   ]
		}
	]
}