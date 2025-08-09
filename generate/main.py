#!/usr/bin/env python3
from __future__ import annotations

import sys
import argparse

import world_tools as world_tools

import logging
logger = logging.getLogger("EWGenerate")
LOG_FILENAME = "EWgenerate.log"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"

def main(world_name: str, log_level: int):
	logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT, filemode="w", level=log_level)
	logging.info('Generator started')
	print('Generator started')
	world = world_tools.TWorld(world_name)
	if not world.generate():
		logging.info(f"- {world_name} is not a world file")
		print(f"- '{world_name}' is not a world file")
	print('Generator stopped')
	logging.info('Generator stopped')

if __name__ == "__main__":
	log_levels: dict = {
		"info": logging.INFO,
		"warning": logging.WARNING,
		"debug": logging.DEBUG
	}

	log_level = logging.INFO # default logging level
	filename: str = "demo" # default world name 

	parser = argparse.ArgumentParser(
		description="Parses and generate world server information.",
		epilog="Author: John Aage Andersen, Reddit: johnaagelv, 2025"
	)
	parser.add_argument("-f", "--filename", help=f"the filename (no ext) of the file holding the definitions", required=True)
	parser.add_argument("-l", "--log_level", help="the logging level to use: 'info' (default), 'warning', or 'debug'", choices=["info","warning","debug", None])
	args = parser.parse_args()

	if args.filename is not None:
		filename = args.filename
	if args.log_level is not None:
		if args.log_level.lower() in log_levels.keys():
			log_level = log_levels[args.log_level.lower()]

	main(filename, log_level)