from __future__ import annotations
#from typing import Tuple
import random
#import generator.tile_types as tile_types
#from generator.tile_types import tile_dt
import opensimplex
import numpy as np
from PIL import Image
#from pathlib import Path
import pickle
from noise import pnoise2
#import matplotlib.pyplot as plt

def get_tile_from_height(val) -> tuple[int, int, int, int]:
	if val < 0:
		val = 0
	if val > 255:
		val = 255 - random.randint(0,2)

	if val <= 84:
		if random.random() > 0.5:
			return (0, 62, 178, 255)
		return (0, 54, 170, 255)
	elif val <= 102:
		return (9, 82, 198, 255)
	elif val <= 112:
		return (254, 224, 179, 255)
	elif val <= 134:
		return (9, 120, 93, 255)
	elif val <= 164:
		return (10, 107, 72, 255)
	elif val <= 200:
		return (11, 94, 51, 255)
	elif val <= 224:
		return (140, 142, 123, 255)
	elif val <= 242:
		return (160, 162, 143, 255)
	elif val <= 253:
		return (200, 202, 193, 255)
	return (255, 255, 255, 255)

def height_map(
	heightMap: np.ndarray,
	seed: int,
	start_x: int,
	start_y: int,
	w: int,
	h: int,
	bias: int=2,
	scale: float=100,
	octaves: int=6,
	persistence: float=0.5,
	lacunarity: float=2.0,
	start_amplitude: float=1.0,
	start_frequency: float=1.0,
	variance: int = 2,
	overlap: bool = False
) -> None: #np.ndarray:
	"""
	HEIGHT MAP
	"""
	scale_w = w / 4
	scale_h = h / 4
	noise = opensimplex.OpenSimplex(seed=seed)
	for x in range(w):
		for y in range(h):
			amplitude = start_amplitude
			frequency = start_frequency
			noiseHeight = 0

			for _ in range(0, octaves):
				sampleX = x / scale_w * frequency
				sampleY = y / scale_h * frequency

				value = noise.noise2(sampleX, sampleY)
				noiseHeight += value * amplitude + random.random() * 0.01 - 0.005

				amplitude *= persistence
				frequency *= lacunarity
				heightMap[start_x + x, start_y + y] = (noiseHeight + 1) * 128

			# Circular square mask
			distX = max(0, min(abs(w / 2 - x), w))
			distY = max(0, min(abs(h / 2 - y), h))
			dist = max(distX, distY)

			# Applying mask
			maxWidth = min(w, h) / 2 - bias
			delta = dist / maxWidth
			gradient = delta ** variance
			heightMap[start_x + x, start_y + y] *= max(0.0, 1.0 - gradient)
#	return heightMap

def gen_map(w:int, h: int, scale: float=100, octaves: int=6, persistence: float=0.5, lacunarity: float=2.0) -> np.ndarray:
	map = np.empty((w, h), order="F")
	for x in range(w):
		for y in range(h):
			map[x][y] = pnoise2(
				x / scale,
				y / scale,
				octaves=octaves,
				persistence=persistence,
				lacunarity=lacunarity,
				repeatx=w,
				repeaty=h,
				base=42
			)
	return map

def main():
#	name: str
	maps: list[dict]
	world_width: int
	world_height: int
	with open("server/data/ankt.dat", "rb") as f:
		data = pickle.load(f)
#		name = data["name"]
		maps = data["maps"]
		print(f"World size {data['width']},{data['height']}")
		world_width = data["width"]
		world_height = data["height"]

	w = maps[0]["width"]
	h = maps[0]["height"]
	colour_map = np.zeros((w * world_width, h * world_height, 4), dtype=np.uint8, order="C")
	for wx in range(world_width):
		for wy in range(world_height):
			map_idx = wx * world_height + wy
			map = maps[map_idx]["tiles"]
			for x in range(w):
				for y in range(h):
					colour = map["light"][x, y][1]
#					colour_map[wx * w + x, wy * h + y] = colour
					colour_map[wy * h + y, wx * w + x] = colour
	image = Image.fromarray(colour_map, 'RGBA')
	image.show()
	exit()

	w = 400
	h = 400
	colour_map = np.zeros((w, h, 4), dtype=np.uint32, order="F")
	heightMap = np.empty((w, h), dtype=np.short, order="F")
	"""
	generator_name, map_idx, seed, bias, octaves, persistance, lacunarity, amplitude, frequency
	"""
	height_map(
		heightMap, 
		seed=189,
		start_x=100, 
		start_y=100, 
		w=300, 
		h=250, 
		bias=10, 
		octaves=11, 
		persistence=0.6, 
		lacunarity=2.0, # Larger to lesser islands
		start_amplitude=1.4, 
		start_frequency=1.0,
		variance=12,
	)
	height_map(
		heightMap, 
		seed=2189,
		start_x=5, 
		start_y=5, 
		w=40, 
		h=40, 
		bias=2, 
		octaves=6, 
		persistence=0.6, 
		lacunarity=1.0, # Larger to lesser islands
		start_amplitude=1.0, 
		start_frequency=1.0,
		variance=2,
	)
	height_map(
		heightMap, 
		seed=12189,
		start_x=18, 
		start_y=50, 
		w=72, 
		h=72, 
		bias=0, 
		octaves=6, 
		persistence=0.6, 
		lacunarity=0.8, # Larger to lesser islands
		start_amplitude=1.2, 
		start_frequency=1.0,
		variance=2,
	)
	height_map(
		heightMap, 
		seed=12189,
		start_x=78, 
		start_y=4, 
		w=58, 
		h=58, 
		bias=0, 
		octaves=6, 
		persistence=0.6, 
		lacunarity=0.8, # Larger to lesser islands
		start_amplitude=1.2, 
		start_frequency=0.8,
		variance=4,
	)
	for x in range(w):
		for y in range(h):
			colour_map[y, x] = get_tile_from_height(heightMap[x, y])
	image = Image.fromarray(colour_map, 'RGBA')
	image.show()


if __name__ == "__main__":
	main()