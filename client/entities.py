from typing import Dict, Optional
import logging
logger = logging.getLogger("EWClient")

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

	@property
	def world(self) -> TWorld:
		logger.debug(f"TActor->world")
		return self.data["world"]
	
	@property
	def map(self):
		logger.debug(f"TActor->map")
		return self.world.maps[self.data["m"]]

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

	def run(self) -> Optional[Dict]:
		logger.debug(f"TActor->run()")
		request = None
		
		# When the actor is on a map, the default command is Field Of Sense (FOS)
		logger.debug(f"- map_idx = {self.map_idx}")
		if self.map_idx >= 0:
			request = {
				"cmd": "fos",
				"x": self.data["x"],
				"y": self.data["y"],
				"z": self.data["z"],
				"m": self.data["m"],
				"r": self.data["r"],
			}
		else:
			request = {
				"cmd": "new",
			}
		logger.debug(f"- request: {request!r}")
		return request