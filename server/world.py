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
		self.world = {
			"name": "Demo",
			"author": "JAA",
			"maps": ["Home","City","Country"],
		}
		with open('server/data/'+name+'.json', 'wt') as f:
			json.dump(self.world, f)

#		with open('server/data/'+name+'.json', 'rt') as f:
#			self.world = json.load(f)
		
		print(f"World started for {self.world['name']} by {self.world['author']}")
		
#		for map in self.world['maps']:
#			with open('server/data/'+map+'.map', 'rb') as f:
#				self.maps.append(pickle.load(f))
		
		print(f"World loaded, {len(self.world['maps'])} maps")

	def fov(self, x:int, y: int, z: int, r: int = 1):
		return list()

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
