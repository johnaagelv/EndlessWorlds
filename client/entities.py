from typing import Dict

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
