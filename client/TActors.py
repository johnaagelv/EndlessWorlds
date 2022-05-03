"""
TActor is any character in the game
"""
class TActor:
	def __init__(self):
		# States holds the current value of the player states
		self.states = {
			"world" : {
				"ip" : "127.0.0.1",
				"port" : 50000,
			},
			"position" : {
				"x" : 0, # X coordinate in the map
				"y" : 0, # Y coordinate in the map
				"z" : 0, # Index of the current map in the world
			},
		}
		self.is_running = True

		# Behaviours are activities that the player may be able to do
		self.behaviours = {}

	@property
	def is_playing(self) -> bool:
		return self.is_running

	def run():
		pass

