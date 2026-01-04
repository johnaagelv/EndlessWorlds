from __future__ import annotations

import uuid
import json
import pickle
import random
import math

from pathlib import Path
from typing import Callable

import generator.tile_types as tile_types
import tcod.tileset

import generator.item_types as item_types

import numpy as np
import logging
logger = logging.getLogger("EWGenerate")
world_data: dict = {
	"name": str,
	"world_width": int,
	"world_height": int,
	"maps": list,
	"entries": list,
	"gateways": list
}

type commandFn = Callable[[list], None]

def generate(filename: Path) -> None:
	logger.info(f"generate( {filename} )")
	with open(filename, "rt") as f:
		build_instructions = json.load(f)
	
	world_data["name"] = build_instructions["name"]
	world_data["entries"] = build_instructions["entries"]
	world_data["maps"] = []

	for build in build_instructions["builds"][0]:
		generator_name = build[0]
		generator = generators.get(generator_name)
		if generator:
			generator(build)

	logger.info("- saving")
	with open("server/data/ankt.dat", "wb") as f:
		print(f"World size {world_data["world_width"]},{world_data["world_height"]}")
		save_data = {
			"name": world_data["name"],
			"width": world_data["world_width"],
			"height": world_data["world_height"],
			"entry": world_data["entries"],
			"maps": world_data["maps"]
		}
		pickle.dump(save_data, f)

def get_tile_by_name(name: str) -> np.ndarray:
#	logger.info(f"get_tile_by_name( {name} )")
	try:
		tile = tile_types.tiles[name]
		logger.debug(tile)
	except Exception:
		logger.warning(
			f"- tile {name} not found among tile types! Using tile 'blank' instead!"
		)
		tile = tile_types.tiles['blank']
	return tile

def gen_world(build: list) -> None:
	""" Generate a world as a collection of maps """
	logger.info(f"generate_world( {build} )")
	generator_name: str = build[0]
	map_width: int = build[1]
	map_height: int = build[2]
	world_data["world_width"] = build[3]
	world_data["world_height"] = build[4]
	map_tiles: list = build[5]
	# seed = build[6]
	for ww in range(0, world_data["world_width"]):
		for wh in range(0, world_data["world_height"]):
			gen_map([generator_name, map_width, map_height, map_tiles, True, ww, wh, True])

def gen_map(build: list) -> None:
	""" Generate a single map """
	logger.info(f"generate_map( {build} )")
	# 0=name, 1=width, 2=height, 3=tiles, 4=visible, 5=ww, 6=wh, 7=Overworld, 8=name (optional)
	map_tile = get_tile_by_name(build[3][0])
	ww = build[5]
	wh = build[6]
	map_name = f"Quadrant {ww} {wh}"
	if len(build) > 8:
		map_name = build[8]
	map_width = build[1]
	map_height = build[2]
	map_visibility = build[4]
	tile_count = len(build[3])

	map: dict = {
		"name": map_name,
		"ww": ww,
		"wh": wh,
		"overworld": build[7],
		"width": map_width,
		"height": map_height,
		"tiles": np.full((map_width, map_height), fill_value=map_tile, order="F"),
		"gateways": list,
		"actions": list,
		"visible": map_visibility,
		"items": list,
		"actors": list
	}
	# randomize tiles
	if tile_count > 1:
		for x in range(0, map_width):
			for y in range(0, map_height):
				map["tiles"][x, y] = get_tile_by_name(build[3][random.randint(0,tile_count - 1)])
	
	# Initialize the lists to ensure append will work
	map['items'] = []
	map['actors'] = []
	map['gateways'] = []
	map['actions'] = []
	world_data["maps"].append(map)

def gen_circle(build: list) -> None:
	""" Generate a circular area with a border of a tile or filled with a tile """
	# 0=name, 1=map_idx, 2=x, 3=y, 4=radius, 4=tiles, 5=fill, 6=thickness
	logger.info(f"gen_circle( {build!r} )")
	if len(build) < 8:
		logger.error(f"- too few build parameters! {len(build)} given")
		raise SystemError
	name, map_idx, center_x, center_y, radius, tiles, fill, thickness = build
	map_tile = get_tile_by_name(tiles[0])
	if fill:
		for r in range(0, 360, 1):
			r_angle = math.radians(r)
			x = center_x + int(math.sin(r_angle) * radius)
			y = center_y + int(math.cos(r_angle) * radius)
			if min(center_x, x) >= 0 and max(center_x, x) <= world_data["maps"][map_idx]['width'] and min(center_y, y) >= 0 and max(center_y, y) <= world_data["maps"][map_idx]['height']:
				tile_name = tiles[random.randint(0,len(tiles) - 1)]
				map_tile = get_tile_by_name(tile_name)
				world_data["maps"][map_idx]['tiles'][min(center_x, x):max(center_x, x), min(center_y, y):max(center_y, y)] = map_tile
	else:
		thickness = max(thickness, 1)
		for r in range(0, 360):
			r_angle = math.radians(r)
			for t in range(0, thickness):
				x = center_x + int(math.sin(r_angle) * (radius - t))
				y = center_y + int(math.cos(r_angle) * (radius - t))
				if min(center_x, x) >= 0 and max(center_x, x) < world_data["maps"][map_idx]['width'] and min(center_y, y) >= 0 and max(center_y, y) < world_data["maps"][map_idx]['height']:
					tile_name = tiles[random.randint(0,len(tiles) - 1)]
					map_tile = get_tile_by_name(tile_name)
					world_data["maps"][map_idx]['tiles'][x, y] = map_tile

""" Generators to be used for building a world """
generators: dict[str, commandFn] = {
	"world": gen_world,
	"map": gen_map,
	"circle": gen_circle
}

gateway_list: list[dict]

class TWorld:
	maps: list = []
	name: str
	entry: list

	def __init__(self, world_name: str) -> None:
		logger.info(f"TWorld->__init__( world_name='{world_name}' )")
		self.filename = world_name

	def generate(self) -> bool:
		logger.info("generate()")
		with open("generator/definitions/" + self.filename + ".json", "rt") as f:
			build = json.load(f)

		# Check that a name is in there!		
		if "name" not in build:
			return False

		map_idx: int = 0
		self.name = build["name"]
		self.entry = build["entry"]
		for map in build["maps"]:
			for build in map:
				if build[0] == 0:
					self.maps.append(self.gen_map(build))
					map_idx = len(self.maps)-1
					logging.info(f"- map idx {map_idx} for {self.maps[map_idx]['name']}")
				elif build[0] == 1:
					self.gen_square(map_idx, build)
				elif build[0] == 2:
					self.gen_circle(map_idx, build)
				elif build[0] == 3:
					self.gen_gateway(map_idx, build)
				elif build[0] == 4:
					self.gen_gateway(map_idx, build)
				elif build[0] == 5:
					self.gen_area(map_idx, build)
				elif build[0] == 6:
					self.gen_trail(map_idx, build)
				elif build[0] == 7:
					self.gen_sym(map_idx, build)
				elif build[0] == 8:
					self.gen_item_tile(map_idx, build)
				elif build[0] == 9:
					self.gen_gateway_border(map_idx, build)
				elif build[0] == 1000: # Items
					self.gen_item(map_idx, build)
				else:
					logger.error(f"ERROR: unhandled type {build[0]}")
			
		self.save()
		return True

	def save(self):
		logger.info("TWorld->save()")
		with open("server/data/" + self.filename + '.dat', "wb") as f:
			save_data = {
				"name": self.name,
				"entry": self.entry,
				"maps": self.maps
			}
			pickle.dump(save_data, f)
	
	def get_tile_by_name(self, name: str) -> np.ndarray:
#		logger.info(f"get_tile_by_name( {name} )")
		try:
			tile = tile_types.tiles[name]
		except Exception:
			logger.warning(
				f"- tile {name} not found among tile types! Using tile 'blank' instead!"
			)
			tile = tile_types.tiles['blank']
		return tile


	def gen_map(self, build: dict) -> dict:
		logger.info("")
		logger.info(f"gen_map( {build!r} )")
		# Always start with the first tile
		map_tile = self.get_tile_by_name(build[4][0])
		tile_count = len(build[4])
		map_name = build[1]
		map_width = build[2]
		map_height = build[3]
		map_visibility = build[5]
		try:
			random.seed(build[6])
		except Exception:
			pass

		map: dict = {
			"name": map_name,
			"width": map_width,
			"height": map_height,
			"tiles": np.full((map_width, map_height), fill_value=map_tile, order="F"),
			"gateways": list,
			"actions": list,
			"visible": map_visibility,
			"items": list,
			"actors": list
		}
		# randomize tiles
		if tile_count > 1:
			for x in range(0, map_width):
				for y in range(0, map_height):
					map["tiles"][x, y] = self.get_tile_by_name(build[4][random.randint(0,tile_count - 1)])

		# Initialize the lists to ensure append will work
		map['items'] = []
		map['actors'] = []
		map['gateways'] = []
		map['actions'] = []
		return map

	"""
	Add the specified tile to a world map
	"""
	def gen_tile(self, map_idx: int, build: dict):
		# 0=tile, 1=x, 2=y, 3=tile
		logger.info(f"gen_tile( {build!r} )")
		map_tile = self.get_tile_by_name(build[3])
		tile_x = build[1]
		tile_y = build[2]
		self.maps[map_idx]['tiles'][tile_x, tile_y] = map_tile

	"""
	1. Generate a square/rectangle with a border of a tile or filled with a tile
	"""
	def gen_square(self, map_idx: int, build: dict):
		logger.info(f"gen_square( {build!r} )")
		if len(build) < 7:
			logger.error(f"- too few build parameters! {len(build)} given")
			raise SystemError()
		# Use first tile as default
		map_tile = self.get_tile_by_name(build[5][0])
		tile_count = len(build[5])
		x1 = build[1]
		y1 = build[2]
		x2 = x1 + build[3]
		y2 = y1 + build[4]
		fill = build[6]
		if fill:
			if tile_count > 1:
				for x in range(x1, x2):
					for y in range(y1, y2):
						self.maps[map_idx]["tiles"][x, y] = self.get_tile_by_name(build[5][random.randint(0,tile_count - 1)])
			else:
				self.maps[map_idx]['tiles'][x1:x2, y1:y2] = map_tile
		else:
			for y in range(y1, y2):
				self.maps[map_idx]['tiles'][x1, y] = self.get_tile_by_name(build[5][random.randint(0,tile_count - 1)])
				self.maps[map_idx]['tiles'][x2-1, y] = self.get_tile_by_name(build[5][random.randint(0,tile_count - 1)])
			for x in range(x1, x2):
				self.maps[map_idx]['tiles'][x, y1] = self.get_tile_by_name(build[5][random.randint(0,tile_count - 1)])
				self.maps[map_idx]['tiles'][x, y2-1] = self.get_tile_by_name(build[5][random.randint(0,tile_count - 1)])

	"""
	2. Generate a circular area with a border of a tile or filled with a tile
	"""
	def gen_circle(self, map_idx: int, build: dict):
		# 0=circle, 1=x, 2=y, 3=radius, 4=tile, 5=fill, 6=thickness
		logger.info(f"gen_circle( {build!r} )")
		if len(build) < 7:
			logger.error(f"- too few build parameters! {len(build)} given")
			raise SystemError()
		map_tile = self.get_tile_by_name(build[4])
		center_x = build[1]
		center_y = build[2]
		radius = build[3]
		fill = build[5]
		if fill:
			for r in range(0, 360, 1):
				r_angle = math.radians(r)
				x = center_x + int(math.sin(r_angle) * radius)
				y = center_y + int(math.cos(r_angle) * radius)
				if min(center_x, x) >= 0 and max(center_x, x) <= self.maps[map_idx]['width'] and min(center_y, y) >= 0 and max(center_y, y) <= self.maps[map_idx]['height']:
					tile_name = build[4][random.randint(0,len(build[4]) - 1)]
					map_tile = self.get_tile_by_name(tile_name)
					self.maps[map_idx]['tiles'][min(center_x, x):max(center_x, x), min(center_y, y):max(center_y, y)] = map_tile
		else:
			thickness = 1
			if len(build) >= 7:
				thickness = max(build[6], 1)
			for r in range(0, 360):
				r_angle = math.radians(r)
				for t in range(0, thickness):
					x = center_x + int(math.sin(r_angle) * (radius - t))
					y = center_y + int(math.cos(r_angle) * (radius - t))
					if min(center_x, x) >= 0 and max(center_x, x) < self.maps[map_idx]['width'] and min(center_y, y) >= 0 and max(center_y, y) < self.maps[map_idx]['height']:
						tile_name = build[4][random.randint(0,len(build[4]) - 1)]
						map_tile = self.get_tile_by_name(tile_name)
						self.maps[map_idx]['tiles'][x, y] = map_tile

	"""
	3. Generate an movement activated gateway to a location on another map
	4. Generate an action activated gateway to a location on another map
	"""
	def gen_gateway(self, map_idx: int, build: dict):
		# Creates gateways and stairways and other map shifting tiles
		# 0=gateway, 1=x, 2=y, 3=tile, 4=x, 5=y, 6=z, 7=map_idx, 8=direction up/down
		logger.info(f"gen_gateway( {build!r} )")
		if (build[0] == 3 and len(build) < 8) or (build[0] == 4 and len(build) < 9):
			logger.error(f"- too few build parameters! {len(build)} given")
			raise SystemError()
		self.gen_tile(map_idx, build)
		tile_x = build[1]
		tile_y = build[2]
		target_x = build[4]
		target_y = build[5]
#		target_z = build[6]
		target_m = build[7]
		user_action = None
		target_host: str = ""
		if len(build) > 8:
			user_action = build[8]
		if len(build) > 9:
			target_host = build[9]

		self.maps[map_idx]['gateways'].append(
			{
				"x": tile_x,
				"y": tile_y,
				"action": user_action,
				"gateway": {
					"x": target_x,
					"y": target_y,
					"m": target_m,
					"h": target_host
				}
			}
		)

	"""
	5. Generate an area of up to 3 tiles based on chances
	Used for building forest, plains, space ...
	"""
	def gen_area(self, map_idx: int, build: dict):
		logger.info(f"gen_area( {build!r} )")
		if len(build) < 7:
			logger.error(f"- too few build parameters! {len(build)} given")
			raise SystemError()
		map_tile1 = self.get_tile_by_name(build[5])
		map_tile2 = self.get_tile_by_name(build[6])
		tile_chance1 = 0.75
		tile_chance2 = 0.5
		try:
			map_tile3 = self.get_tile_by_name(build[7])
		except Exception:
			map_tile3 = self.get_tile_by_name('blank')
		try:
			logger.info("- parse tile chances from 7")
			tile_chance1 = float(int(build[7]) / 100)
			tile_chance2 = float(int(build[8]) / 100)
		except Exception:
			try:
				logger.info("- parse tile chances from 8")
				tile_chance1 = float(int(build[8]) / 100)
				tile_chance2 = float(int(build[9]) / 100)
			except Exception:
				pass
		logger.info(f"- tile chances {tile_chance1}, {tile_chance2}")
		x1 = build[1]
		y1 = build[2]
		x2 = x1 + build[3]
		y2 = y1 + build[4]
		for x in range(x1, x2):
			for y in range(y1, y2):
				chance = random.random()
				if chance > tile_chance1:
					self.maps[map_idx]['tiles'][x, y] = map_tile1
				elif chance > tile_chance2:
					self.maps[map_idx]['tiles'][x, y] = map_tile2
				else:
					self.maps[map_idx]['tiles'][x, y] = map_tile3

	"""
	6. Generate a trail of tiles in the longest direction (up/down or left/right)
	Used for generating tunnels, rivers, ...
	"""
	# [6, 46, 21, 450, 21, 2, 8, "floor"]
	def gen_trail(self, map_idx: int, build: dict):
		logger.info(f"gen_trail( {build!r} )")
		if len(build) < 8:
			logger.error(f"- too few build parameters! {len(build)} given")
			raise SystemError()
		map_tile = self.get_tile_by_name(build[7])
		x1 = build[1]
		y1 = build[2]
		x2 = build[3]
		y2 = build[4]
		w1 = build[5]
		w2 = build[6]
		try:
			random.seed(build[8])
		except Exception:
			pass
		if abs(x1 - x2) > abs(y1 - y2): # x axis is longest
			y_step = abs(y1 - y2) / abs(x1 - x2)
			y = float(y1)
			y_start = min(y1, y2)
			y_stop = max(y1, y2)
			trail_width = random.randint(w1, w2)
			trail_direction = random.randint(-5, 5)
			x_start = min(x1, x2)
			x_stop = max(x1, x2)
			for x in range(x_start, x_stop):
				chance = random.random()
				if chance > 0.7:
					trail_width = random.randint(w1, w2)
					d_min = -2
					d_max = 2
					if y < trail_width * 2:
						d_min = 1
						d_max = 3
					if y > self.maps[map_idx]['height'] - trail_width * 2:
						d_min = -3
						d_max = -1
					if x > int(x_stop / 3) and y < y_stop:
						d_min = 0
						d_max = 3
					if x > int(x_stop / 3) and y > y_stop:
						d_min = -3
						d_max = 0
					trail_direction = random.randint(d_min, d_max)
				
				self.maps[map_idx]['tiles'][x, int(y) - trail_width:int(y) + trail_width] = map_tile
				y += y_step + trail_direction
				if y < trail_width * 2 or y > self.maps[map_idx]['height'] - trail_width * 2:
					trail_direction = -trail_direction
		else: # y axis is longest
			x_step = abs(x1 - x2) / abs(y1 - y2)
			x = float(x1)
			x_start = min(x1, x2)
			x_stop = max(x1, x2)
			trail_width = random.randint(w1, w2)
			trail_direction = random.randint(-5, 5)
			y_start = min(y1, y2)
			y_stop = max(y1, y2)
			for y in range(y_start, y_stop):
				chance = random.random()
				if chance > 0.7:
					trail_width = random.randint(w1, w2)
					d_min = -2
					d_max = 2
					if x < trail_width * 2:
						d_min = 1
						d_max = 3
					if x > self.maps[map_idx]['width'] - trail_width * 2:
						d_min = -3
						d_max = -1
					if y > int(y_stop / 3) and x < x_stop:
						d_min = 0
						d_max = 3
					if y > int(y_stop / 3) and x > x_stop:
						d_min = -3
						d_max = 0
					trail_direction = random.randint(d_min, d_max)
				
				self.maps[map_idx]['tiles'][int(x) - trail_width:int(x) + trail_width, y] = map_tile
				x += x_step + trail_direction
				if x < trail_width * 2 or x > self.maps[map_idx]['width'] - trail_width * 2:
					trail_direction = -trail_direction

	"""
	7. Generate all the charmap tiles. Used for testing the tilesheet
	"""
	def gen_sym(self, map_idx: int, build: dict):
		sym = 0
		for y in range(0,16,2):
			for x in range(0, 64, 2):
				sym_char = tcod.tileset.CHARMAP_CP437[sym]
				map_tile = tile_types.new_tile(
					walkable=True,
					transparent=True,
					dark=(sym_char, (255, 255, 255, 255), (0, 0, 0, 255)),
					light=(sym_char, (255, 255, 255, 255), (0, 0, 0, 255)),
					gateway=False,
				)
				self.maps[map_idx]['tiles'][x, y] = map_tile
				del(map_tile)
				print(f"{x},{y} = {sym} = {sym_char}")
				sym += 1

	"""
	8. Generate a tile of an item with user actions
	"""
	def gen_item_tile(self, map_idx: int, build: dict):
		# Creates items with attached actions
		# 0=item, 1=x, 2=y, 3=tile, 4=actions
		logger.info(f"gen_item_tile( {build!r} )")
		if len(build) < 5:
			logger.error(f"- too few build parameters! {len(build)} given")
			raise SystemError()
		# Add the tile to the map
		self.gen_tile(map_idx, build)
		tile_x: int = build[1]
		tile_y: int = build[2]
		user_actions: dict = build[4]

		self.maps[map_idx]['actions'].append(
			{
				"x": tile_x,
				"y": tile_y,
				"actions": user_actions,
			}
		)
	"""
	9. Generate a border gateway
	"""
	def gen_gateway_border(self, map_idx: int, build: dict) -> None:
		# Create a X or Y border gateway
		# 9=border, target map, X or Y
		logger.info(f"gen_gateway_border( {build!r} )")
		if build[3] == "x":
			for y in range(0, self.maps[map_idx]["height"]):
				self.maps[map_idx]["gateways"].append(
					{
						"x": build[1],
						"y": y,
						"action": None,
						"gateway": {
							"x": build[4],
							"y": y,
							"m": build[2],
						}
					}
				)
				self.maps[map_idx]["tiles"][build[1],y]["gateway"] = True

		if build[3] == "y":
			for x in range(0, self.maps[map_idx]["width"]):
				self.maps[map_idx]["gateways"].append(
					{
						"x": x,
						"y": build[1],
						"action": None,
						"gateway": {
							"x": x,
							"y": build[4],
							"m": build[2],
						}
					}
				)
				self.maps[map_idx]["tiles"][x, build[1]]["gateway"] = True


	"""
	1000. Generate an item
	"""
	def gen_item(self, map_idx: int, build: dict) -> None:
		# Creates an item
		# 1000=x, y, w, h, n, item name, where n is the count per tile
		logger.info(f"gen_item( {build!r} )")
		x = build[1]
		y = build[2]
		w = build[3]
		h = build[4]
		count = build[5]
		for tile_x in range(x, x + w):
			for tile_y in range(y, y + h):
				for _ in range(0, count):
					self.maps[map_idx]["items"].append(
						{
							"x": tile_x,
							"y": tile_y,
							"iid": uuid.uuid4(),
							"face": item_types.items[build[6]]["face"],
							"name": item_types.items[build[6]]["name"],
							"fg": item_types.items[build[6]]["fg"],
							"bg": item_types.items[build[6]]["bg"],
						}
					)
