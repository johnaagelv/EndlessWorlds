from __future__ import annotations

import pickle
from typing import Tuple
from pathlib import Path
import logging
logger = logging.getLogger("EWlogger")

class TWorld:
	"""
	The world class manages:
	- several maps representing the world.
	- actors who travels the world (cid, x, y, z, m)
	- several entry points for new players of the world
	"""
	name: str
	maps: list[dict]
	entry_points: list
	actors: dict
	items: list

	def __init__(self, filename: Path):
		logger.info(f"TWorld->__init__({filename})")
		with open(filename, "rb") as f:
			data = pickle.load(f)
			self.name = data["name"]
			self.maps = data["maps"]
			self.entry_points = data["entry"]
			self.actors = {}
			self.items = []
		logger.debug(self.entry_points)

	def get_world_definition(self) -> list:
		"""
		Get world definition
		- collects and returns the name, size, visibility, and may include the FOS, of all the maps
		"""
		logger.info("TWorld->get_world_definition()")
		map_sizes: list = []
		for map_index, map in enumerate(self.maps):
			fos: dict = {}
			if map["visible"]:
				fos = self.get_map_field_of_sense(map_index, 0, 0, 0, True)
			map_sizes.append({
				"name": map["name"],
				"width": self.get_map_width(map_index),
				"height": self.get_map_height(map_index),
				"visible": map["visible"],
				"fos": fos,
				"gateways": self.get_map_gateways(map_index),
				"items": self.get_map_items(map_index),
			})
		return map_sizes

	def get_world_entry_points(self) -> list:
		"""
		Get world entry points
		- retrieves and returns the world entry points, where a new player can be located
		"""
		logger.info("TWorld->get_world_entry_points()")
		return self.entry_points

	# NOTE: get_map_by_index is not used!
	def get_map_by_index(self, map_index: int) -> dict:
		logger.debug(f"TWorld->get_map_by_index({map_index})")
		return self.maps[map_index]

	def get_map_size(self, map_index: int) -> Tuple[int, int]:
		"""
		Get map size
		- retrieves and returns the size (width and height) of the specified map
		"""
		logger.debug(f"TWorld->get_map_size({map_index})")
		return self.maps[map_index]["width"], self.maps[map_index]["height"]
	
	def get_map_width(self, map_index: int) -> int:
		"""
		Get map width
		- retrieves and returns the width (x axis) of the specified map
		"""
		logger.debug(f"TWorld->get_map_width({map_index})")
		return self.maps[map_index]["width"]

	def get_map_height(self, map_index: int) -> int:
		"""
		Get map height
		- retrieves and returns the height (y axis) of the specified map
		"""
		logger.debug(f"TWorld->get_map_height({map_index})")
		return self.maps[map_index]["height"]

	def get_map_gateways(self, map_index: int) -> dict:
		"""
		Get map gateways
		- retrieves and returns the gateways of the specified map
		"""
		logger.debug(f"TWorld->get_map_gateways({map_index})")
		return self.maps[map_index]["gateways"]
	
	def get_map_items(self, map_index: int) -> list:
		"""
		Get map items
		- retrieves and returns the items of the specified map
		"""
		logger.debug(f"TWorld->get_map_items({map_index})")
		return self.maps[map_index]['items']

	def get_map_tile_slice(self, map_index: int, x_min: int = 0, x_max: int = 0, y_min: int = 0, y_max: int = 0) -> list:
		"""
		Get map tile slice
		- retrieves and returns a slice of tiles of the specified map
		"""
		logger.debug(f"TWorld->get_map_tile_slice({map_index}, {x_min}, {x_max}, {y_min}, {y_max})")
		return self.maps[map_index]["tiles"][x_min:x_max, y_min:y_max]

	def _calculate_field_of_sense(self, map_index: int, x: int, y: int, r: int, visible: bool = False) -> Tuple[int, int, int, int]:
		"""
		Calculate field of sense (fos)
		- calculates a map slice dimensions as the x and y axes minimum and maximum values based on the specified point (x, y), radius and visibility indication
		returns the calculated map slice dimensions
		"""
		map_width, map_height = self.get_map_size(map_index)
		if visible or r == 0: # Get the full map
			x_min = 0
			x_max = map_width
			y_min = 0
			y_max = map_height
		else: # Get a slice of the map
			x_min = max(x - r, 0)
			x_max = min(x + r + 1, map_width)
			y_min = max(y - r, 0)
			y_max = min(y + r + 1, map_height)
		return x_min, x_max, y_min, y_max
	
	def get_items_in_field_of_sense(self, map_index: int, x_min: int, x_max: int, y_min: int, y_max: int) -> list:
		"""
		Get items in field of sense (fos)
		- retrieves and returns a list of the itmes within the specified map slice
		"""
		logger.debug("TWorld->get_items_in_field_of_sense(...)")
		return [item for item in self.maps[map_index]["items"] if x_min <= item["x"] <= x_max and y_min <= item["y"] <= y_max]

	def get_actors_in_field_of_sense(self, map_index: int, x_min: int, x_max: int, y_min: int, y_max: int) -> list:
		"""
		Get actors in field of sense (fos)
		- retrieves and returns a list of the actors within the specified map slice
		"""
		logger.debug(f"TWorld->get_actors_in_field_of_sense({map_index}, {x_min}, {x_max}, {y_min}, {y_max})")
		actors: list = []
		for actor_cid in self.actors:
			actor = self.actors[actor_cid]
			if x_min <= actor["x"] <= x_max and y_min <= actor["y"] <= y_max and actor["m"] == map_index:
				actors.append(actor) #{"cid": actor_cid, "x": actor['x'], "y": actor['y'], "face": actor["face"]})
		return actors
		#return [actor for actor in self.actors if x_min <= actor[0]["x"] <= x_max and y_min <= actor[0]["y"] <= y_max and actor["m"] == map_index]

	def get_map_field_of_sense(self, map_index: int, x: int, y: int, r: int, visible: bool = False) -> dict:
		"""
		Get map field of sense (fos)
		- calculates the map slice dimensions
		- retrieves the map slice
		- retreives the map gateways, as they may have changed
		- retrieves the list of actors within the map slice
		returns all of the above as one dict collection
		"""
		logger.debug(f"TWorld->get_map_field_of_sense({map_index},{x}, {y}, {r}, {visible})")
		x_min, x_max, y_min, y_max = self._calculate_field_of_sense(map_index, x, y, r, visible)
		
		fos: dict = {
			"x_min": x_min,
			"x_max": x_max,
			"y_min": y_min,
			"y_max": y_max,
			"view": self.get_map_tile_slice(map_index, x_min, x_max, y_min, y_max),
			"gateways": self.get_map_gateways(map_index),
			"actors": self.get_actors_in_field_of_sense(map_index, x_min, x_max, y_min, y_max),
			"items": self.get_items_in_field_of_sense(map_index, x_min, x_max, y_min, y_max),
		}
		return fos
	
	def set_map_tile(self, map_index: int, x: int, y: int, tile: None) -> None:
		logger.debug(f"set_map_tile({map_index}, {x}, {y}, {tile})")
