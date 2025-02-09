from typing import Dict, List, Tuple

import colours as colour

class TDataManager:
	"""
	This data manager controls the data in structure as defined:
	0 [ key : value ] m
	0 [ node : 1 [ key : value ] m ] n
	"""
	data: Dict

	def __init__(self):
		self.data = {
			"actor": {
				"face": "@",
				"colour": colour.white,
				"name": "<unknown>",
			},
			"location": {
				"x": 0, # X
				"y": 0, # Y
				"z": 0, # Height 
				"m": 0, # Map index
			},
			"world": {
				"ip": "0.0.0.0:12345",
			}
		}
	
	def set(self, *, node: str = None, key: str, value: str | int | Dict | Tuple | List) -> None:
		key = key.lower()
		if node is None:
			self.data[key] = value

		else:
			node = node.lower()
			if node in self.data:
				self.data[node][key] = value

			else:
				self.data[node] = {key: value}
		




	