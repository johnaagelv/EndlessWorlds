#!/usr/bin/env python3
import numpy as np

from tcod.console import Console
import tcod

import tile_types

class TMap:
	def __init__(self, width: int, height: int):
		self.width = width
		self.height = height
		self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")
		self.tiles[30:33, 22] = tile_types.wall
	
	def inbounds(self, x: int, y: int) -> bool:
		return 0 <= x < self.width and 0 <= y < self.height
	
	def render(self, console: Console) -> None:
		console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]


def main():
	screen_width = 80
	screen_height = 50
	map_width = 80
	map_height = 45
	tileset = tcod.tileset.load_tilesheet(
		"dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
	)
	pass

if __name__ == "__main__":
	main()