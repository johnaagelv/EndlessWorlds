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
```
	"character":
	{
		"face": "@",
		"colour": [255, 255, 255]
	},
```
- face - a symbol that represents the character
- colour - an rgb colour applied to the face symbol

## States collection
The current collection is defined as shown below:
```
	"states":
	{
		"health":
		{
			"value": 10000,
			"max": 10000,
			"min": 0
		},
		"energy":
		{
			"value": 10000,
			"max": 10000,
			"min": 0
		}
	},
```
- health - defines the healt current value, the max and the min health value

## Location collection
The current collection is defined as shown below:
```
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
```
- world - defines the connection to the world server and the world name
- map - indicates the map number within the world
- x, y, z - defines the characters position in the map as x, y, z where x, y are the 2D location and z is the height

## Memories collection
The current collection is defined as shown below:
```
	"memories":
	{
		"maps":
		[
			{
				"name": "Landing camp",
				"width": 80,
				"height": 45,
				"explored": null
			}
		]
	},
```

## Effects collection
The current collection is defined as shown below:
```
	"effects":
	[
		{
			"scope": "states",
			"key": "health",
			"name": "poisoned",
			"ticks": 100,
			"value": -1,
		}
	]
```
Each effect is short-lived, meaning that effects will terminate after some time.
With the above effect on the health state as an example:
- scope - indicates which collection the effect is to be applied to
- key - indicates that the health state is to be affected
- name - name of the effect
- ticks - how much time the effect is in effect. This is decreased for every tick. When reaching 0 (zero) the effect is ended
- value - a value that is applied every tick to the health value while it is in effect

The poison effect above will be active for 100 ticks and lower the health state by 1 every tick.

For a single time effect, like eating food to raise the energy state, a tick of 1 would be used!

Other effect ideas could be to have the max change, to allow for boosting a state.