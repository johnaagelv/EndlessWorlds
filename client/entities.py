import time

from connectors import TConnector

"""
Entity represents the player or NPC
"""
class TEntity:
	"""
	A generic object to represent players, enemies, items, etc.
	"""
	def __init__(self, client: TConnector):
		self.tick = time.time()
		self.client = client

	def load(self, data):
		self.data = data

	"""
	Process one scope [effects, ...]
	"""
	def _process(self, scope):
		if scope in self.data:
			for item in self.data[scope]:
				self.data[item["scope"]][item["key"]]["value"] += item["value"]
				item["ticks"] -= 1

				if item["ticks"] == 0:
					del(item)

	def run(self):
		if time.time() - self.tick > 5:
			self._process("effects")
			self._process("conditions")
			self.tick = time.time()
