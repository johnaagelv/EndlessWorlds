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
			map_width = int(map_definition.get("width"))
			map_height = int(map_definition.get("height"))
			map_visible = map_definition.get('visible')
			self.maps.append(
				{
					"width": map_width,
					"height": map_height,
					"tiles": np.full((map_width, map_height), fill_value=tile_types.floor, order="F"),
					"visible": np.full((map_width, map_height), fill_value=map_visible, order="F"),
					"explored": np.full((map_width, map_height), fill_value=map_visible, order="F"),
				}
			)
			if map_visible:
				fos = map_definition.get("fos")
				temp = fos.get("view")
				view = np.array(temp)
				self.maps[-1]["tiles"][0:map_width, 0:map_height] = view


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