import json

def main():

	data = {
		"playing": True,
		"character": {
			"face": "@",
			"colour": (255, 255, 255),
		},
		"states": {
			"health": {
				"value": 10000, # Value represents 100.00
				"max": 10000,
				"min": 0,
			},
		},
		"location": {
			"w": { # World information: server and name
				"host": "192.168.1.104",
				"port": 65432,
				"name": "Ankt"
			},
			"m": 0, # Map number in the world
			"x": 15, # X coordinate in the map
			"y": 15, # Y coordinate in the map
			"z": 0, # Height in the map
		},
		"memories": { # Player or NPC memories
			"maps": [ # Map memories in the current world
				{
					"name": "",
					"width": 80,
					"height": 45,
					"explored": None,
				}
			]
		},
		"effects": [ # Effects that changes states, a dynamic list
			{ # This effect affects the health state by -1 for every tick in 100 ticks time, eq a -100 change over time
				"scope": "states", # Scope identifies the affected area
				"key": "health", # Key identifies the affected item
				"name": "poisoned", # Name identifies the effect
				"ticks": 100, # ticks is how many ticks this effect will be in force
				"change": -1, # change is how much the item value is affected per tick
				"fixed": 0, # fixed is how much the item value is changed during the time of ticks
				# Usually only one of "change" or "fixed" is defined/used
			},
		],
	}

	with open("client/save.sav","wt") as f:
		f.write(json.dumps(data))

if __name__ == "__main__":
	main()