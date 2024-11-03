#import numpy as np
#import pickle
#import socket
#import config

#from typing import Tuple
from connectors import TConnector

"""
Entity represents the player or NPC
"""
class TEntity:
	"""
	A generic object to represent players, enemies, items, etc.
	"""
	def __init__(self, client: TConnector):
		self.client = client

	def load(self, data):
		self.data = data
