from typing import Dict, List, TYPE_CHECKING
import logging
logger = logging.getLogger("EWClient")

import numpy as np
import json

from tcod.console import Console
if TYPE_CHECKING:
	from entities import TActor

import tile_types

class numpy_array_encoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.ndarray):
			return obj.tolist()
		return json.JSONEncoder.default(self, obj)

class TWorld:
	maps: List = []

	def __init__(self, actor, map_definitions):
		logger.debug(f"TWorld->__init__( actor, map_definitions )")
		logger.debug(f"- map_definitions {map_definitions!r}")
		self.actor: TActor = actor
		for map_definition in map_definitions:
			self.maps.append(
				{
					"width": map_definition["width"],
					"height": map_definition["height"],
					"tiles": np.full((map_definition["width"],map_definition["height"]), fill_value=tile_types.floor, order="F"),
					"visible": np.full((map_definition["width"],map_definition["height"]), fill_value=map_definition['visible'], order="F"),
					"explored": np.full((map_definition["width"],map_definition["height"]), fill_value=map_definition['visible'], order="F"),
				}
			)

	def in_bounds(self, x: int, y: int, m: int) -> bool:
		logger.debug(f"TWorld->in_bounds( x, y, m )")
		return 0 <= x < self.maps[m]["width"] and 0 <= y < self.maps[m]["height"]

	def in_gateway(self, x: int, y: int, m: int) -> bool:
		logger.debug(f"TWorld->in_gateway( x, y, m )")
		return self.maps[m]["tiles"][x, y]["gateway"]
	
	def go_gateway(self, x: int, y: int, m: int):
		logger.debug(f"TWorld->go_gateway( x, y, m )")
		gateway = next((item for item in self.maps[m]["gateways"] if item["x"] ==x and item["y"] == y), None)
		return gateway