from typing import Dict, Optional, Tuple
import logging
logger = logging.getLogger("EWClient")

from tcod.map import compute_fov

from worlds import TWorld


class TEntity:
	data: Dict = {}
	def __init__(self, data):
		logger.debug(f"TEntity->__init__( data )")
		self.data = data

class TActor(TEntity):
	def __init__(self, data):
		logger.debug(f"TActor->__init__( data )")
		super().__init__(data)
		self.fos = None

	"""
	Provide the World
	"""
	@property
	def world(self) -> TWorld:
		logger.debug(f"TActor->world")
		return self.data["world"]
	
	"""
	Provide the current map
	"""
	@property
	def map(self):
		logger.debug(f"TActor->map")
		return self.world.maps[self.map_idx]

	"""
	Provide the map index
	"""
	@property
	def map_idx(self) -> int:
		logger.debug(f"TActor->map_idx")
		return self.data["m"]

	@property
	def me(self):
		logger.debug(f"TActor->me")
		return self.data
	
	@property
	def is_playing(self) -> bool:
		logger.debug(f"TActor->is_playing")
		return self.data["playing"]
	
	@property
	def current_xy(self) -> Tuple[int, int]:
		logger.debug(f"TActor->current_xy")
		return self.data['x'], self.data['y']
	
	def capability(self, capability: str):
		logger.debug(f"TActor->capability( capability={capability} )")
		return self.data['capabilities'][capability][0]

	def run(self) -> Optional[Dict]:
		logger.debug(f"TActor->run()")
		request = None
		map_idx = self.map_idx
		
		# When the actor is on a map, the default command is Field Of Sense (FOS)
		if map_idx >= 0:
			request = {
				"cmd": "fos",
				"x": self.data["x"],
				"y": self.data["y"],
				"z": self.data["z"],
				"m": map_idx,
				"r": self.capability('vision'),
			}
		else:
			request = {
				"cmd": "new",
			}
		logger.debug(f"- request: {request!r}")
		return request

	def update_fos(self) -> None:
		self.map['visible'][:] = compute_fov(
			self.map['tiles']['transparent'],
			(self.data['x'], self.data['y']),
			radius = self.capability('vision')
		)
		self.map['explored'] |= self.map['visible']