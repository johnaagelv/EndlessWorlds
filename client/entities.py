from typing import Dict, Optional

from worlds import TWorld

class TEntity:
	data: Dict = {}
	def __init__(self, data):
		self.data = data

class TActor(TEntity):
	def __init__(self, data):
		super().__init__(data)
		self.fos = None

	@property
	def world(self) -> TWorld:
		return self.data["world"]
	
	@property
	def map(self):
		return self.world.maps[self.data["m"]]

	@property
	def map_idx(self) -> int:
		return self.data["m"]

	@property
	def me(self):
		return self.data
	
	@property
	def is_playing(self) -> bool:
		return self.data["playing"]

	def run(self) -> Optional[Dict]:
		request = None
		
		if self.map_idx() >= 0:
			request = {
				"cmd": "fos",
				"x": self.data["x"],
				"y": self.data["y"],
				"z": self.data["z"],
				"m": self.data["m"],
				"r": self.data["r"],
			}
		return request