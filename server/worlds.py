from __future__ import annotations

from typing import Dict, List
import pickle
import random
import logging
logger = logging.getLogger("EWlogger")

import numpy as np

import tile_types

class TWorld:
	maps: list = []
	name: str
	entry: list = []

	def __init__(self, world_name: str = 'world'):
		logger.debug(f"TWorld->init({world_name})")
		self.name = world_name
		with open(world_name + ".dat", "rb") as f:
			load_data = pickle.load(f)

		self.entry = load_data['entry']
		self.maps = load_data['maps']
		print(f"- running {world_name} with {len(self.maps)} maps.")

	"""
	# Get and return the field of sense
	"""
	def field_of_sense(self, fos_request: dict, visible: bool = False) -> dict:
		logger.debug(f"TWorld->field_of_sense({fos_request!r})")
		# Extract the fos parameters m, x, y, z, r
		if fos_request is not None:
			m: int = fos_request["m"] # Map number
		x: int = fos_request["x"] # x coordinate on map m
		y: int = fos_request["y"] # y coordinate on map m
		# z = fos_request.get("z") # z coordinate = height on map m (not yet used)
		r: int = fos_request["r"] # r radius
		if visible:
			x_min = 0
			x_max = self.maps[m]["width"]
			y_min = 0
			y_max = self.maps[m]["height"]
		else:
			x_min = max(x - r, 0)
			x_max = min(x + r + 1, self.maps[m]["width"])
			y_min = max(y - r, 0)
			y_max = min(y + r + 1, self.maps[m]["height"])

		logger.debug(f"FOS of {x_min}:{x_max}, {y_min}:{y_max}")
		fos = {
			"x_min": x_min,
			"x_max": x_max,
			"y_min": y_min,
			"y_max": y_max,
			"view": self.maps[m]["tiles"][x_min:x_max, y_min:y_max],
			"gateways": self.maps[m]["gateways"]
		}

		return fos
	
	"""
	Get and return the map sizes for a new player
	"""
	def map_definitions(self) -> List:
		logger.debug(f"TWorld->map_sizes()")
		map_sizes: list = []
		for map_idx, m in enumerate(self.maps):
			fos: dict | None = None
			if m["visible"]:
				fos = self.field_of_sense({"x":0, "y": 0, "z": 0, "m": map_idx, "r": 0}, True)
			map_sizes.append(
				{
					"name": m["name"],
					"width": m["width"],
					"height": m["height"],
					"visible": m["visible"],
					"fos": fos
				}
			)
		return map_sizes
	
	"""
	Get one random entry point of the world for new player
	"""
	def entry_point(self) -> Dict:
		logger.debug(f"TWorld->entry_point()")
		# Random randint() method https://www.w3schools.com/python/ref_random_randint.asp
		return self.entry[random.randint(0, len(self.entry)-1)] # Randint includes both start and stop values
