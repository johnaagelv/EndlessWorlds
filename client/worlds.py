from typing import Dict, List

import numpy as np
import json

from tcod.console import Console

import tile_types

class numpy_array_encoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.ndarray):
			return obj.tolist()
		return json.JSONEncoder.default(self, obj)

class TWorld:
	maps: List = []

	def __init__(self):
		self.maps.append(
			{
				"name": "Survey base",
				"width": 80,
				"height": 45,
				"tiles": np.full((80, 45), fill_value=tile_types.floor, order="F"),
				"gateways": [],
			}
		)
		self.maps.append(
			{
				"name": "Underground",
				"width": 80,
				"height": 45,
				"tiles": np.full((80, 45), fill_value=tile_types.floor, order="F"),
				"gateways": [],
			}
		)

		self.maps[0]["tiles"][0, 0:45] = tile_types.wall
		self.maps[0]["tiles"][79, 0:45] = tile_types.wall
		self.maps[0]["tiles"][0:80, 0] = tile_types.wall
		self.maps[0]["tiles"][0:80, 44] = tile_types.wall
		self.maps[0]["tiles"][20:22, 0:45] = tile_types.wall

		self.maps[0]["tiles"][8:12, 10:13] = tile_types.wall
		self.maps[0]["tiles"][10, 10]["gateway"] = True
		self.maps[0]["tiles"][10, 10] = tile_types.gate
		self.maps[0]["gateways"].append(
			{
				"x": 10,
				"y": 10,
				"gateway": {
					"x": 10,
					"y": 10,
					"m": 1
				}
			}
		)

		self.maps[0]["tiles"][44:47, 9:11] = tile_types.wall
		self.maps[0]["tiles"][45, 10]["gateway"] = True
		self.maps[0]["tiles"][45, 10] = tile_types.gate
		self.maps[0]["gateways"].append(
			{
				"x": 45,
				"y": 10,
				"gateway": {
					"x": 45,
					"y": 10,
					"m": 1
				}
			}
		)

		self.maps[1]["tiles"][44:47, 10:12] = tile_types.wall
		self.maps[1]["tiles"][45, 10]["gateway"] = True
		self.maps[1]["tiles"][45, 10] = tile_types.gate
		self.maps[1]["gateways"].append(
			{
				"x": 45,
				"y": 10,
				"gateway": {
					"x": 45,
					"y": 10,
					"m": 0
				}
			}
		)

		self.maps[1]["tiles"][9:12, 10:12] = tile_types.wall
		self.maps[1]["tiles"][10, 10]["gateway"] = True
		self.maps[1]["tiles"][10, 10] = tile_types.gate
		self.maps[1]["gateways"].append(
			{
				"x": 10,
				"y": 10,
				"gateway": {
					"x": 10,
					"y": 10,
					"m": 0
				}
			}
		)

	def in_bounds(self, x: int, y: int, m: int) -> bool:
		return 0 <= x < self.maps[m]["width"] and 0 <= y < self.maps[m]["height"]

	def in_gateway(self, x: int, y: int, m: int) -> bool:
		return self.maps[m]["tiles"][x, y]["gateway"]
	
	def go_gateway(self, x: int, y: int, m: int):
		gateway = next((item for item in self.maps[m]["gateways"] if item["x"] ==x and item["y"] == y), None)
		return gateway["gateway"]
	
	def render(self, console: Console, m: int) -> None:
		console.rgb[0:self.maps[m]["width"], 0:self.maps[m]["height"]] = self.maps[0]["tiles"]["dark"]

	def save(self):
		world = []

		for map in self.maps:
			world.append(map["name"])
			with open(map["name"]+".map", "wt") as fmap:
				data = {
					"name": map["name"],
					"width": map["width"],
					"height": map["height"],
					"tiles": map["tiles"],
					"gateways": map["gateways"],
				}
				fmap.write(json.dumps(data, cls=numpy_array_encoder))

		with open("World.map", "wt") as fworld:
			fworld.write(json.dumps(world))
