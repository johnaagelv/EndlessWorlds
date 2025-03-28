from typing import Dict, List
import logging
logger = logging.getLogger("EWlogger")

import numpy as np

import tile_types

class TWorld:
	maps: List = []

	def __init__(self, world_name: str = 'world'):
		logger.debug("TWorld->init()")
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
		self.maps[0]["tiles"][20:22, 10:45] = tile_types.wall

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

	"""
	# Get and return the field of sense
	"""
	def field_of_sense(self, fos_request: Dict) -> Dict:
		logger.debug(f"TWorld->field_of_sense({fos_request!r})")
		# Extract the fos parameters m, x, y, z, r
		m = fos_request.get("m") # Map number
		x = fos_request.get("x") # x coordinate on map m
		y = fos_request.get("y") # y coordinate on map m
		# z = fos_request.get("z") # z coordinate = height on map m (not yet used)
		r = fos_request.get("r") # r radius

		x_min = max(x - r, 0)
		x_max = min(x + r + 1, self.maps[m]["width"])
		y_min = max(y - r, 0)
		y_max = min(y + r + 1, self.maps[m]["height"])

		fos = {
			"x_min": x_min,
			"x_max": x_max,
			"y_min": y_min,
			"y_max": y_max,
			"view": self.maps[m]["tiles"][x_min:x_max, y_min:y_max],
			"gateways": self.maps[m]["gateways"]
		}

		return fos
