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
- senses - collection of properties defining the character's senses, such as vision, ..., etc.
- effects - collection of properties defining the character's active effects, such as poisoned, ..., etc.
- conditions - collection of properties defining the character's active conditions, which may affect other properties

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
- colour - an RGB colour applied to the face symbol

## States collection
The states collection is defined as shown below and every state is optional:
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
		},
		...
	},
```
- health - defines the healt current value, the max and the min health value
- energy - defines the energy current value, the max and the min energy value

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
The effects collection is defined as shown below and can contain 0 (zero) to many effects:
```
	"effects":
	[
		{
			"scope": "states",
			"key": "health",
			"name": "poisoned",
			"ticks": 100,
			"value": -1,
		},
		...
	]
```
With the above effect on the health state as an example:
- scope - indicates which collection the effect is to be applied to
- key - indicates that the health state is to be affected
- name - name of the effect (optional)
- ticks - how much time the effect is in effect. This is decreased for every tick. When reaching 0 (zero) the effect is ended
- value - a value that is applied every tick to the health value while it is in effect

The poison effect above will be active for 100 ticks and lower the health state by 1 every tick.

For a single time effect, like eating food to raise the energy state, a tick of 1 would be used!
Example below
```
		{
			"scope": "states",
			"key": "energy",
			"name": "eating",
			"ticks": 1
			"value": 10
		}
```

A blinding effect could be defined as the example below:
```
		{
			"scope": "senses",
			"key": "vision",
			"name": "blinded",
			"ticks": 10,
			"range": -10
		}
```
The above effect would affect a range of 0 for 10 ticks, simulating blindness!

Other effect ideas could be to have the max change, to allow for boosting a state.

## Senses collection
The senses collection is defined as shown below.
```
	"senses":
	{
		"vision": {
			"value": 4.
			"max": 4,
			"min": 0
		},
		"hearing": {
			"value": 4.
			"max": 4,
			"min": 0
		},
		"smelling": {
			"value": 4.
			"max": 4,
			"min": 0
		},
		...
	}
```
Currently a sense only has a value for which it is effective. The value is a radius of tiles from the character's location (x,y)
	
The max and min properties are used in case an effect will be applied to a sense, so that the range later can
be returned to its max value when the effect ends.

## Conditions collection
The conditions collection is processed for each tick and can invoke one or more effects.

```
	"conditions": [
		{
			"scope": "states",
			"key": "health",
			"less": 50,
			"invoke": [
				"effect": {
					"scope": "states",
					"key": "energy",
					"name": "not feeling well",
					"ticks": 1,
					"value": -1
				}
			]
		},
		{
			"scope": "states",
			"key": "health",
			"greater": 50,
			"invoke": [
				"effect": {
					"scope": "states",
					"key": "energy",
					"name": "",
					"ticks": 1,
					"value": 1
				}
			]
		}
	]
```
The above conditions defines that the energy state changes:
- when the health state value is less than 50 by deducting 1 from the energy state value
- when the health state value is greater than 50 by adding 1 to the energy state value
