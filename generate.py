#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import generator.world_tools as world_tools

import logging
logger = logging.getLogger("EWGenerate")
LOG_FILENAME = "EWgenerate.log"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"

def main(world_name: str, log_level: int, task: str) -> None:
	logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT, filemode="w", level=log_level)
	logging.info('Generator started')
	print('Generator started')
	match(task):
		case "new":
#			world_tools.new_world(world_name)
			world_tools.generate(Path(f"generator/definitions/{world_name}.json"))
#			world_tools.save_map()
		case "add":
#			world_tools.load_map()
#			world_tools.add(Path(f"generator/definitions/{world_name}.json"))
			pass
		case "save":
#			world_tools.load_map()
#			world_tools.build_map(Path(f"generator/definitions/{world_name}.map"))
			pass
	
	print('Generator stopped')
	logging.info('Generator stopped')

if __name__ == "__main__":
	log_levels: dict = {"info": logging.INFO, "warning": logging.WARNING, "debug": logging.DEBUG}
	task_list: dict = {"new": "new", "add": "add", "save": "save"}

	log_level = logging.INFO # default logging level
	filename: str = "demo" # default world name 
	task: str = "new"

	parser = argparse.ArgumentParser(
		description="Parses and generate world server information.",
		epilog="Author: John Aage Andersen, Reddit: johnaagelv, 2025"
	)
	parser.add_argument("-f", "--filename", help="the filename (no ext) of the file holding the definitions", required=True)
	parser.add_argument("-t", "--task", help="task to perform: new, update, save", choices=["new", "add", "save", None])
	parser.add_argument("-l", "--log_level", help="the logging level to use: 'info' (default), 'warning', or 'debug'", choices=["info","warning","debug", None])
	args = parser.parse_args()

	if args.filename is not None:
		filename = args.filename
	if args.task is not None:
		if args.task.lower() in task_list.keys():
			task = task_list[args.task.lower()]
	if args.log_level is not None:
		if args.log_level.lower() in log_levels.keys():
			log_level = log_levels[args.log_level.lower()]

	main(filename, log_level, task)