#!/usr/bin/env python3
from typing import Dict, List
import math
import pickle
import json
import numpy as np
import tile_types

class TWorld:
	maps: List = []
	name: str
	entry: List

	def save(self):
		with open(self.name + '.dat', "wb") as f:
			save_data = {
				"name": self.name,
				"entry": self.entry,
				"maps": self.maps
			}
			pickle.dump(save_data, f)
			

def get_tile_by_name(name) -> np.array:
	try:
		tile = tile_types.tiles[name]
	except:
		print(f"ERROR: Tile {name} not found among tile types!")
		print(f"- using tile 'blank' instead!")
		tile = tile_types.tiles['blank']
	return tile

def gen_world(build) -> TWorld:
	print(f"world {build['name']}")
	world = TWorld()
	world.name = build["name"]
	world.entry = build["entry"]
	return world

def gen_map(build) -> Dict:
	print(f"map {build[1]}, size {build[2]},{build[3]}")
	map_tile = get_tile_by_name('blank')
	map_name = build[1]
	map_width = build[2]
	map_height = build[3]
	map = {
		"name": map_name,
		"width": map_width,
		"height": map_height,
		"tiles": np.full((map_width, map_height), fill_value=map_tile, order="F"),
		"gateways": [],
	}
	return map

def gen_square(world: TWorld, map_idx: int, build):
	print(f"- square ({build[1]},{build[2]}), ({build[3]},{build[4]}) as {build[5]}, fill={build[6]}")
	map_tile = get_tile_by_name(build[5])
	x1 = build[1]
	y1 = build[2]
	x2 = x1 + build[3]
	y2 = y1 + build[4]
	fill = build[6]
	if fill:
		world.maps[map_idx]['tiles'][x1:x2, y1:y2] = map_tile
	else:
		world.maps[map_idx]['tiles'][x1, y1:y2] = map_tile
		world.maps[map_idx]['tiles'][x2-1, y1:y2] = map_tile
		world.maps[map_idx]['tiles'][x1:x2, y1] = map_tile
		world.maps[map_idx]['tiles'][x1:x2, y2-1] = map_tile

def gen_circle(world: TWorld, map_idx: int, build):
	print(f"- circle ({build[1]},{build[2]}) radius {build[3]} as {build[4]}, fill={build[5]}")
	map_tile = get_tile_by_name(build[4])
	center_x = build[1]
	center_y = build[2]
	radius = int(build[3])
	fill = build[5]
	if fill:
		for r in range(0, 360):
			x = center_x + int(math.sin(r) * radius)
			y = center_y + int(math.cos(r) * radius)
			world.maps[map_idx]['tiles'][min(center_x, x):max(center_x, x), min(center_y, y):max(center_y, y)] = map_tile
	else:
		for r in range(0, 360):
			x = center_x + int(math.sin(r) * radius)
			y = center_y + int(math.cos(r) * radius)
			world.maps[map_idx]['tiles'][x, y] = map_tile

def gen_tile(world: TWorld, map_idx: int, build):
	print(f"- tile ({build[1]},{build[2]}) as {build[3]}")
	map_tile = get_tile_by_name(build[3])
	tile_x = build[1]
	tile_y = build[2]
	world.maps[map_idx]['tiles'][tile_x, tile_y] = map_tile

def gen_gateway(world: TWorld, map_idx: int, build):
	# Creates gateways and stairwais and other map shifting tiles
	print(f"- gateway ({build[1]},{build[2]}) as {build[3]} target ({build[4]},{build[5]}) in map {build[7]}")
	gen_tile(world, map_idx, build)
	tile_x = build[1]
	tile_y = build[2]
	target_x = build[4]
	target_y = build[5]
	target_z = build[6]
	target_m = build[7]
	world.maps[map_idx]['gateways'].append(
		{
			"x": tile_x,
			"y": tile_y,
			"gateway": {
				"x": target_x,
				"y": target_y,
				"m": target_m
			}
		}
	)	

def main():
	with open("generate/ankt.gen", "rt") as f:
		world_definition = json.load(f)
		world = gen_world(world_definition)

		for build in world_definition["maps"]:
			if build[0] == 0:
				world.maps.append(gen_map(build))
				map_idx = len(world.maps)-1
			elif build[0] == 1:
				gen_square(world, map_idx, build)
			elif build[0] == 2:
				gen_circle(world, map_idx, build)
			elif build[0] == 3:
				gen_gateway(world, map_idx, build)
			elif build[0] == 4:
				gen_gateway(world, map_idx, build)
		
		print(f"World {world.name} with {map_idx+1} maps")
		#tmp = input('Enter:')
	
		world.save()

if __name__ == "__main__":
	main()