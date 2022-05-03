from typing import Dict
from TServers import TServer
from TActors import TActor

"""
TAction classes are the local actions performed by the actor (player, npc)
"""
class TAction:
	def __init__(self):
		pass

	def run(self, actor: TActor):
		raise NotImplementedError()

"""
TServerAction classes are the integrator between the actor (player, npc) and the world server
"""
class TServerAction(TAction):
	def __init__(self, server: TServer):
		super().__init__()
		self.server = server


"""
TGameNewAction initializes the player for a new game
"""
class TGameNewAction(TAction):
	def run(self, actor: TActor):
		pass

"""
TGameLoadAction initializes the player for a saved game
"""
class TGameLoadAction(TAction):
	def __init__(self, choice: Dict):
		super().__init__()
		self.choice = choice

	def run(self, actor: TActor):
		pass

"""
TGameQuitAction marks the player for stopping the current game
"""
class TGameQuitAction(TAction):
	def run(self, actor: TActor):
		actor.states["play"] = False


"""
TMoveAction takes a request from the actor to move from its current position to a target position.
It queries the World server for permission to perform the move
"""
class TMoveAction(TAction):
	def run(self, actor):
		pass

