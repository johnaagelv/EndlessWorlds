#!/usr/bin/env python3
from typing import Dict, List
import json
import numpy as np
import tile_types

class TWorld:
	maps: List = []
	name: str

def gen_world(build) -> TWorld:
	print(f"world {build['name']}")
	world = TWorld()
	world.name = build["name"]
	return world

def gen_map(build) -> Dict:
	print(f"map {build[1]}, size {build[2]},{build[3]}")
	map = {
		"name": build[1],
		"width": build[2],
		"height": build[3],
		"tiles": np.full((build[2], build[3]), fill_value=tile_types.tiles['blank'], order="F"),
		"gateways": [],
	}
	return map

def gen_square(map, build):
	print(f"square ({build[1]},{build[2]}), ({build[3]},{build[4]}) as {build[5]})")
	map['tiles'][build[1]:build[2],build[3]:[build[4]]] = tile_types.tiles[build[5]]

def gen_circle(map, build):
	print(f"circle ({build[1]},{build[2]}) radius {build[3]} as {build[4]} of {build[5]}")

def main():
	with open("generate/ankt.gen", "rt") as f:
		world_definition = json.load(f)
		world = gen_world(world_definition)

		for build in world_definition["maps"]:
			if build[0] == 0:
				world.maps.append(gen_map(build))
				map_idx = len(world.maps)-1
			elif build[0] == 1:
				gen_square(world.maps[map_idx], build)
			elif build[0] == 2:
				gen_circle(world.maps[map_idx], build)
		
		print(f"World {world.name} with {map_idx+1} maps")

if __name__ == "__main__":
	main()