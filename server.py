#!/usr/bin/env python3
from __future__ import annotations

import server.utils as utils
import argparse
from pathlib import Path

import server.game_server as server
#from server.worlds import TWorld
from server.world import TWorld

import logging
logger = logging.getLogger("EWlogger")
LOG_FILENAME = Path("EWserver.log")
LOG_LEVEL = logging.INFO

SERVER_PORT: int = 25261
SERVER_HOST: str = "127.0.0.1"

def main(port: int, log_level: int, world_name: Path):
	logging.basicConfig(filename=LOG_FILENAME, format="%(asctime)s %(levelname)-8s %(message)s", filemode="w", level=log_level)
	logger.info('World server started')
	print('World server started')

	host = utils.get_local_ip()

	if world_name == "":
		world_configuration = utils.get_config('world')
		world_name = world_configuration['name']

	world = TWorld(world_name)
	server.init(host, port)

	try:
		while True:
			server.run(world)

	except KeyboardInterrupt:
		server.server_selector.close()

	logger.info('World server stopped')
	print('World server stopped')

if __name__ == "__main__":
	log_levels = {'info': logging.INFO, 'debug': logging.DEBUG}
	port: int = SERVER_PORT
	log_level: int = LOG_LEVEL
	filename = Path('data/demo.dat')

	parser = argparse.ArgumentParser(
		description="Runs a multiplayer Roguelike World server.",
		epilog="Author: John Aage Andersen, Reddit: johnaagelv, 2025"
	)
	parser.add_argument("-p", "--port", help=f"the port number to use, default is {SERVER_PORT}")
	parser.add_argument("-l", "--log_level", help="the logging level to use: 'info' (default) or 'debug'")
	parser.add_argument("-w", "--world", help="filename of the world to serve")

	args = parser.parse_args()
	if args.port is not None:
		port = int(args.port)
	if args.log_level is not None:
		if args.log_level.lower() in log_levels.keys():
			log_level = log_levels[args.log_level.lower()]
	if args.world is not None:
		filename = args.world.lower()

	main(port, log_level, filename)
