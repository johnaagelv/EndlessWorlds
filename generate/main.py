#!/usr/bin/env python3
from __future__ import annotations

import sys
import json

import world_tools as world_tools

import logging
logger = logging.getLogger("EWGenerate")
LOG_FILENAME = "EWgenerate.log"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"

def main(world_name: str, log_level: int):
	logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT, filemode="w", level=log_level)
	logging.info('World generator started')
	world = world_tools.TWorld(world_name)
	world.generate()
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