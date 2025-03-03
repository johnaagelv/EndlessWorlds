from typing import Dict, List

import numpy as np
import json

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

	def field_of_sense(self, x: int, y: int, z: int, m: int, r: int):
		map = self.maps[m]
		x1 = max(x - r, 0)
		x2 = min(x + r + 1, map["width"])
		y1 = max(y - r, 0)
		y2 = min(y + r + 1, map["height"])
		fos = map["tiles"][x1:x2,y1:y2]
		return fos
