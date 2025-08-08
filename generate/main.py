#!/usr/bin/env python3
from __future__ import annotations

import sys
import json

import build_tools as bt

import logging
logger = logging.getLogger("EWGenerate")
LOG_FILENAME = "EWgenerate.log"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"

def main(world_name: str, log_level: int):
	logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT, filemode="w", level=log_level)
	logging.info('World generator started')
	with open("definitions/" + world_name + ".json", "rt") as f:
		world_definition = json.load(f)
		world = bt.gen_world(world_definition)

		for map in world_definition["maps"]:
			for build in map:
				if build[0] == 0:
					world.maps.append(bt.gen_map(build))
					map_idx = len(world.maps)-1
					logging.info(f"- map idx {map_idx} for {world.maps[map_idx]['name']}")
				elif build[0] == 1:
					bt.gen_square(world, map_idx, build)
				elif build[0] == 2:
					bt.gen_circle(world, map_idx, build)
				elif build[0] == 3:
					bt.gen_gateway(world, map_idx, build)
				elif build[0] == 4:
					bt.gen_gateway(world, map_idx, build)
				elif build[0] == 5:
					bt.gen_area(world, map_idx, build)
				elif build[0] == 6:
					bt.gen_trail(world, map_idx, build)
				elif build[0] == 7:
					bt.gen_sym(world, map_idx, build)
				elif build[0] == 8:
					bt.gen_item(world, map_idx, build)
				else:
					logger.error(f"ERROR: unhandled type {build[0]}")
		
		world.save()
		logging.info('World generator stopped')

if __name__ == "__main__":
	log_levels: dict = {
		"info": logging.INFO,
		"warning": logging.WARNING,
		"debug": logging.DEBUG
	}

	log_level = logging.INFO # default logging level
	world_name: str = "demo" # default world name 

	try:
		if len(sys.argv) >= 2:
			world_name = sys.argv[1]
			world_name = world_name.lower()

		if len(sys.argv) >= 3:
			log_level_name: str = sys.argv[2]
			log_level = log_levels[log_level_name.lower()]

		if len(sys.argv) < 2 or len(sys.argv) > 4:
			raise SystemError()
	except:
		print(f"Usage: {sys.argv[0]} <world name> <log_level>")
		print(f"  <world name> must be provided")
		print(f"  <log_level> may be info (default), warning, debug")
		sys.exit(1)

	main(world_name, log_level)