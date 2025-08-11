from __future__ import annotations

import logging
logger = logging.getLogger("EWGenerate")

from typing import List
import json
import pickle
import random
import math

import tile_types
import tcod.tileset

import item_types

import numpy as np

class TWorld:
	maps: List = []
	name: str
	entry: List

	def __init__(self, world_name: str) -> None:
		logger.info(f"TWorld->__init__( world_name='{world_name}' )")
		self.filename = world_name

	def generate(self) -> bool:
		logger.info("generate()")
		with open("definitions/" + self.filename + ".json", "rt") as f:
			build = json.load(f)

		# Check that a name is in there!		
		if "name" not in build:
			return False

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
				elif build[0] == 1000: # Items
					self.gen_item(map_idx, build)
				else:
					logger.error(f"ERROR: unhandled type {build[0]}")
			
		self.save()
		return True

	def save(self):
		logger.info(f"TWorld->save()")
		with open("worlds/" + self.filename + '.dat', "wb") as f:
			save_data = {
				"name": self.name,
				"entry": self.entry,
				"maps": self.maps
			}
			pickle.dump(save_data, f)
	
	def get_tile_by_name(self, name: str) -> np.ndarray:
		logger.info(f"get_tile_by_name( {name} )")
		try:
			tile = tile_types.tiles[name]
		except:
			logger.warning(
				f"- tile {name} not found among tile types! Using tile 'blank' instead!"
			)
			tile = tile_types.tiles['blank']
		return tile


	def gen_map(self, build: dict) -> dict:
		logger.info("")
		logger.info(f"gen_map( {build!r} )")
		map_tile = self.get_tile_by_name(build[4])
		map_name = build[1]
		map_width = build[2]
		map_height = build[3]
		map_visibility = build[5]
		try:
			random.seed(build[6])
		except:
			pass

		map = {
			"name": map_name,
			"width": map_width,
			"height": map_height,
			"tiles": np.full((map_width, map_height), fill_value=map_tile, order="F"),
			"gateways": [],
			"actions": [],
			"visible": map_visibility,
			"items": [],
			"actors": []
		}
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
		map_tile = self.get_tile_by_name(build[5])
		x1 = build[1]
		y1 = build[2]
		x2 = x1 + build[3]
		y2 = y1 + build[4]
		fill = build[6]
		if fill:
			self.maps[map_idx]['tiles'][x1:x2, y1:y2] = map_tile
		else:
			self.maps[map_idx]['tiles'][x1, y1:y2] = map_tile
			self.maps[map_idx]['tiles'][x2-1, y1:y2] = map_tile
			self.maps[map_idx]['tiles'][x1:x2, y1] = map_tile
			self.maps[map_idx]['tiles'][x1:x2, y2-1] = map_tile

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
		target_z = build[6]
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
		except:
			map_tile3 = self.get_tile_by_name('blank')
		try:
			logger.info(f"- parse tile chances from 7")
			tile_chance1 = float(int(build[7]) / 100)
			tile_chance2 = float(int(build[8]) / 100)
		except:
			try:
				logger.info(f"- parse tile chances from 8")
				tile_chance1 = float(int(build[8]) / 100)
				tile_chance2 = float(int(build[9]) / 100)
			except:
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
		except:
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
					dark=(sym_char, (255, 255, 255), (0, 0, 0)),
					light=(sym_char, (255, 255, 255), (0, 0, 0)),
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
	1000. Generate an item
	"""
	def gen_item(self, map_idx: int, build: dict) -> None:
		# Creates an item
		# 1000=item, x, y, item name, count to genrate of this item
		logger.info(f"gen_item( {build!r} )")
		count = build[4]
		for _ in range(0, count):
			self.maps[map_idx]["items"].append(
				{
					"x": build[1],
					"y": build[2],
					"item": item_types.items[build[3]]
				}
			)
