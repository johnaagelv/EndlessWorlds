#!/usr/bin/env python3
import sys
import utils
import argparse

from servers import TServer
from worlds import TWorld

import logging
logger = logging.getLogger("EWlogger")
LOG_FILENAME = "EW.log"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
SERVER_PORT = 12345
SERVER_HOST = '127.0.0.1'
log_levels = {'info': logging.INFO, 'debug': logging.DEBUG}

def main(port: int, log_level: int, world_name: str):
	print("World server started")
	logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT, filemode="w", level=log_level)
	logging.info('World server started')

	host = utils.get_local_ip()

	if world_name == "":
		world_configuration = utils.get_config('world')
		world_name = world_configuration['name']

	world = TWorld(world_name)
	server = TServer(host, port, world)
	try:
		while True:
			server.run()

	except KeyboardInterrupt:
		server.sel.close()
		logging.info('World server stopped')
	print("World server stopped")

if __name__ == "__main__":
	port = SERVER_PORT
	log_level = logging.INFO
	world = "demo"

	parser = argparse.ArgumentParser(
		description="Runs a Roguelike World server.",
		epilog="Author: John Aage Andersen, Reddit: johnaagelv, 2025"
	)
	parser.add_argument("-p", "--port", help=f"the port number to use, default is {SERVER_PORT}")
	parser.add_argument("-l", "--log_level", help="the logging level to use: 'info' (default) or 'debug'")
	parser.add_argument("-w", "--world", help="name of the world to serve")
	args = parser.parse_args()
	if args.port is not None:
		port = args.port
	if args.log_level is not None:
		log_level = log_levels[args.log_level]
	if args.world is not None:
		world = args.world

	main(port, log_level, world)
