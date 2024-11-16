# Save file structure
The save file is using json for it data structure and contains information about
the player's properties.

# Properties

## Root level
- playing - boolean value indicating player is playing or not
- character - Collection of properties describing the player
- states - collection of properties defining the character's states, such as health, ..., etc
- location - collection of properties defining the character's location in the world, such as world map, position (x, y, z), ..., etc.
- memories - collection of properties defining the character's memories, such as the world maps, ..., etc.

## Character collection
The current collection is defined as shown below:
'''
	"character":
	{
		"face": "@",
		"colour": [255, 255, 255]
	},
'''
- face - a symbol that represents the character
- colour - an rgb colour applied to the face symbol

## States collection
The current collection is defined as shown below:
'''
	"states":
	{
		"health":
		{
			"value": 10000,
			"max": 10000,
			"min": 0
		}
	},
'''
- health - defines the healt current value, the max and the min health value

## Location collection
The current collection is defined as shown below:
'''
	"location":
	{
		"world":
		{
			"host": "192.168.1.104",
			"port": 65432,
			"name": "Ankt"
		},
		"map": 0,
		"x": 15,
		"y": 15,
		"z": 0
	},
'''
- world - defines the connection to the world server and the world name
- map - indicates the map number within the world
- x, y, z - defines the characters position in the map as x, y, z where x, y are the 2D location and z is the height

## Memories collection
	"memories":
	{
		"maps":
		[
			{
				"name": "",
				"width": 80,
				"height": 45,
				"explored": null
			}
		]
	},
	"effects":
	[
		{
			"scope": "states",
			"key": "health",
			"name": "poisoned",
			"ticks": 100,
			"change": -1,
			"fixed": 0
		}
	]
}