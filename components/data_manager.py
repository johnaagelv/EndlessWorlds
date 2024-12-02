from typing import Dict

import colours as colour

class TDataManager:
	data: Dict

	def __init__(self):
		self.data = {
			"x": 0,
			"y": 0,
			"z": 0,
			"face": "@",
			"colour": colour.white,
			"name": "<unknown>",
		}
	
	def add(self, node: str, key: str, value: str | int) -> None:
		if node in self.data:
			self.data[node][key] = value
		else:
			self.data[node] = {key: value}
		




	