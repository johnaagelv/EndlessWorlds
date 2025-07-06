from typing import Dict, List, TYPE_CHECKING
import logging
logger = logging.getLogger("EWClient")

import numpy as np
import json

if TYPE_CHECKING:
	from entities import TActor

import tile_types

class TMap:
	def __init__(self, map_definition = None, name = None):
		if map_definition is None and name is not None:
			self.load_map(name)
		elif map_definition is not None and name is None:
			self.name = map_definition.get("name")
			self.width = int(map_definition.get("width"))
			self.height = int(map_definition.get("height"))
			self.is_visible = map_definition.get('visible')

			self.tiles = np.full((self.width, self.height), fill_value=tile_types.floor, order="F")
			self.visible = np.full((self.width, self.height), fill_value=self.is_visible, order="F")
			self.explored = np.full((self.width, self.height), fill_value=self.is_visible, order="F")
		else:
			raise NotImplementedError

	def load_map(self, name: str):
		pass

class TWorld:
	maps: list[dict]
	entities: list = []
	map_names: list

	def __init__(self, actor, map_definitions: list):
		logger.info(f"TWorld->__init__( actor={actor}, map_definitions={map_definitions} )")
#		logger.debug(f"- map_definitions {map_definitions!r}")
		self.actor: TActor = actor
#		self.maps: List[Dict | None]
		map_template = {
			"loaded": bool,
			"width": int,
			"height": int,
			"tiles": np.ndarray,
			"visible": np.ndarray,
			"explored": np.ndarray,
			"gateways": list
		}
		map_template['loaded'] = False

		self.map_definitions = map_definitions
		self.maps = [map_template] * len(map_definitions)
#		for map_idx in range(0, len(map_definitions)):
#			self.start_map(map_idx)
		self.start_map(0)

	def start_map(self, map_idx):
		logger.info(f"TWorld->start_map( map_idx={map_idx} )")
		map_idx = self.actor.map_idx
		logger.info(f"- switch to map_idx={map_idx}")
		if self.maps[map_idx]['loaded'] == False:
			logger.info(f" - loading map definition")
			map_definition = self.map_definitions[map_idx]

			map_name = map_definition.get('name')
			map_width = int(map_definition.get("width"))
			map_height = int(map_definition.get("height"))
			map_visible = map_definition.get('visible')
			self.maps[map_idx] = {
				"loaded": True,
				"name": map_name,
				"width": map_width,
				"height": map_height,
				"tiles": np.full((map_width, map_height), fill_value=tile_types.floor, order="F"),
				"visible": np.full((map_width, map_height), fill_value=map_visible, order="F"),
				"explored": np.full((map_width, map_height), fill_value=map_visible, order="F"),
			}

			if map_visible:
				fos = map_definition.get("fos")
				temp = fos.get("view")
				view = np.array(temp)
				if self.maps[map_idx] is not None:
					current_map = self.maps[map_idx]
					if current_map is not None:
						current_map["tiles"][0:map_width, 0:map_height] = view
		
		#self.actor.log.add(self.maps[map_idx]['name'])
		
	def in_bounds(self, x: int, y: int, m: int) -> bool:
		logger.debug(f"TWorld->in_bounds( x={x}, y={y}, m={m} )")
		current_map = self.maps[m]
		if current_map is not None:
			return 0 <= x < current_map["width"] and 0 <= y < current_map["height"]
		return False

	def in_gateway(self, x: int, y: int, m: int) -> bool:
		logger.debug(f"TWorld->in_gateway( x={x}, y={y}, m={m} )")
		logger.info(f"TWorld->in_gateway( x={x}, y={y}, m={m} )")
		current_map = self.maps[m]
		if current_map is not None:
			logger.info(current_map['tiles'][x, y])
			return current_map["tiles"][x, y]["gateway"]
		return False
	
	def go_gateway(self, x: int, y: int, m: int, direction = None):
		logger.info(f"TWorld->go_gateway( x={x}, y={y}, m={m}, direction={direction} )")
		test_map = self.maps[m]
		current_map: Dict
		if test_map is not None:
			current_map = test_map
		gateway_fallback = {
			"gateway": {
				"x": x,
				"y": y,
				"m": m
			}
		}
		if direction is None:
			gateway = next((item for item in current_map["gateways"] if item["x"] == x and item["y"] == y), gateway_fallback)
		else:
			logger.debug(f"- gateways {current_map}")
			gateway = next((item for item in current_map["gateways"] if item["x"] == x and item["y"] == y and item['action'] == direction), gateway_fallback)
		logger.debug(f"- gateway={gateway!r}")
		logger.info(f"- gateway={gateway!r}")
		return gateway