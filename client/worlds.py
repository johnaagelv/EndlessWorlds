from typing import Dict, List

import numpy as np
import json

from tcod.console import Console
from entities import TActor

import tile_types

class numpy_array_encoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.ndarray):
			return obj.tolist()
		return json.JSONEncoder.default(self, obj)

class TWorld:
	maps: List = []

	def __init__(self, actor: TActor):
		self.actor = actor
		pass

	def add_map(self, map_definition: Dict):
		self.maps.append(
			{
				"width": map_definition["width"],
				"height": map_definition["height"],
				"tiles": np.full((map_definition["width"],map_definition["height"]), fill_value=tile_types.SHROUD, order="F"),
				"visible": np.full((map_definition["width"],map_definition["height"]), fill_value=False, order="F"),
				"explored": np.full((map_definition["width"],map_definition["height"]), fill_value=False, order="F"),
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
		console.rgb[0:self.maps[m]["width"], 0:self.maps[m]["height"]] = np.select(
			condlist=[self.maps[m]['visible'], self.maps[m]['explored']],
			choicelist=[self.maps[m]['tiles']['light'], self.maps[m]['tiles']['dark']],
			default=tile_types.SHROUD["dark"],
		)
