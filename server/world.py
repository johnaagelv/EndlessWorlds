from typing import Dict, List, Optional
import json, pickle, uuid
import numpy as np
from dataclasses import dataclass

@dataclass
class TWorldMap:
	name: str
	map: np.array

class TEntity:
	def __init__(self, x: int, y: int, z: int, c: str):
		# Entity location (x, y) in map z
		self.x = x
		self.y = y
		self.x = z
		# Entity representation character (utf-8)
		self.c = c

class TActor(TEntity):
	def __init__(self, x: int, y: int, z: int, c: str, h: str):
		super().__init__(x, y, z, c)
		# Actor host address (ip + port)
		self.h = h
		# Actor unique ID in the world
		self.guid = uuid.uuid4()

class TItem(TEntity):
	def __init__(self, x: int, y: int, z: int, c: str, data: Dict):
		super().__init__(x, y, z, c)
		# Item data
		self.data = data
		# Item unique ID in the world
		self.guid = uuid.uuid4()

class TWorld:
	# All the maps of the world
	maps: List = []
	def __init__(self, name: str = "demo"):
		self.name = name
		self.maps = []
		self.world = {}

		with open('server/'+name+'/world.json', 'rt') as f:
			self.world = json.load(f)
		
		print(f"World started for {self.world['title']} by {self.world['author']}")
		wall = ord("#")
		floor = ord(".")
		the_map = np.array([
			[wall, wall, wall, wall, wall, wall, wall, wall, wall, wall, wall, wall, wall, wall, wall, wall],
			[wall, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, wall],
			[wall, floor, wall, floor, floor, floor, floor, floor, wall, floor, floor, floor, floor, floor, floor, wall],
			[wall, floor, wall, wall, floor, wall, floor, floor, wall, wall, floor, wall, wall, wall, floor, wall],
			[wall, floor, wall, floor, floor, wall, floor, floor, wall, floor, floor, floor, floor, wall, floor, wall],
			[wall, floor, floor, floor, floor, wall, wall, wall, wall, floor, floor, floor, floor, wall, floor, wall],
			[wall, floor, wall, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, wall],
			[wall, floor, wall, wall, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, wall],
			[wall, floor, floor, wall, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, wall],
			[wall, floor, floor, wall, floor, floor, floor, wall, wall, wall, floor, wall, wall, wall, wall, wall],
			[wall, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, wall],
			[wall, wall, wall, wall, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, wall],
			[wall, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, wall],
			[wall, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, wall],
			[wall, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, floor, wall],
			[wall, wall, wall, wall, wall, wall, wall, wall, wall, wall, wall, wall, wall, wall, wall, wall],
		])
		for map in self.world['maps']:
			self.maps.append({"name": map, "width": 16, "height": 16, "map": the_map.tolist()})
		
		for map in self.maps:
			with open('server/data/' + map["name"] + '.map', "wt") as f:
				json.dump(map, f)

		self.maps = []
		for map in self.world['maps']:
			with open('server/data/'+map+'.map', 'rt') as f:
				self.maps.append(json.load(f))
				self.maps[-1]["map"] = np.asarray(self.maps[-1]["map"], order="F") #.reshape(self.maps[-1]["width"], self.maps[-1]["height"], order="F")

		#print(f"{self.maps[0]['map']!r}")

		print(f"World loaded, {len(self.world['maps']) / len(self.maps)} maps")

	def fov(self, x:int, y: int, z: int, r: int = 1):
		x1 = max(0, x - r)
		x2 = min(x + r + 1, self.maps[z]["width"])
		y1 = max(0, y - r)
		y2 = min(y + r + 1, self.maps[z]["height"])
		print(f"{self.maps[z]['map'][x1:x2, y1:y2]!r}")
		fov = self.maps[z].copy()
		fov["width"] = x2 - x1
		fov["height"] = y2 - y1
		fov["map"] = self.maps[z]['map'][x1:x2, y1:y2].tolist()
		return fov

class TEntities:
	def __init__(self):
		self.entities : List[TEntity] = None

	def add_entity(self, entity: TEntity):
		self.entities.append(TEntity)

	def remove_entity_by_guid(self, guid: uuid):
		entity = self.get_by_guid(guid)
		if entity is not None:
			self.entities.remove(entity)

	""" Get an entity (actor or item) based on the GUID """
	def get_by_guid(self, guid: uuid) -> Optional[TEntity]:
		entities = list(filter(lambda entity: entity.guid == guid, self.entities))
		if len(entities) == 0:
			return None
		return entities[0]

	def fov(self, x: int, y: int, z: int, r: int = 1) -> List:
		x1 = x - r
		x2 = x + r
		y1 = y - r
		y2 = y + r
		return list(filter(lambda entity: x1 <= entity.x <= x2 and y1 <= entity.y <= y2 and entity.z == z, self.entities))
