#!/usr/bin/env python3
import random
import numpy as np


class TWorld:
	def __init__(self):
		self.maps = []
		self.generate_demo()

	def generate_demo(self):
		map = np.full((40, 40), fill_value=" ", order="F")
		print(f"{map.size()}")
		x=5
		y=5
		w=20
		h=20
		map[x:x+w-1,y:y+h-1] = self.box(x, y, w, h)
		self.maps.append(map)

		map = np.full((80, 45), fill_value=" ", order="F")
		print(f"{map.size()}")
		x=5
		y=5
		w=10
		h=10
		map[x:x+w-1,y:y+h-1] = self.box(x, y, w, h)
		self.maps.append(map)

		map = np.full((140, 140), fill_value=" ", order="F")
		print(f"{map.size()}")
		x=5
		y=5
		w=10
		h=10
		map[x:x+w-1,y:y+h-1] = self.box(x, y, w, h)
		x=35
		y=5
		w=20
		h=10
		map[x:x+w-1,y:y+h-1] = self.box(x, y, w, h)
		self.maps.append(map)


	def box(self, x: int, y: int, w: int, h: int):
		x1 = x + 1
		x2 = x + w - 2
		y1 = y + 1
		y2 = y + h - 2
		build = np.full((w, h), fill_value="#", order="F")
		build[x1:x2, y1:y2] = " "
		return build