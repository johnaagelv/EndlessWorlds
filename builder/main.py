#!/usr/bin/env python3
import sys
import json
import numpy as np

import build
import construct as cf

def main(args = None):
	with open('server/'+build.build['world']['name']+'/world.json', 'wt') as f:
		json.dump(build.build['world'], f)

	for map_name in build.build['world']['maps']:
		# start the map
		map = np.full( (build.build[map_name]['width'], build.build[map_name]['height']), fill_value=" ", order="F")

		for item in build.build[map_name]['map']:

			if item['type'] == 'accessway':
				cf.build_accessway(map, item)

			if item['type'] == 'circle':
				cf.build_circle(map, item)

			if item['type'] == 'square':
				cf.build_square(map, item)


		with open('server/'+build.build['world']['name']+'/'+map_name+'.json', 'wt') as f:
			json.dump(map.tolist(), f)
	
		#print(f"{map_name}: {map!r}")
		for y in range(0,41):
			row = ""
			for x in range(0,41):
				row += map[x, y]
			print(f"{row}")
		

if __name__ == "__main__":
	main()