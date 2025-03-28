#!/usr/bin/env python3
import sys
import utils

from servers import TServer
from worlds import TWorld

import logging
logger = logging.getLogger("EWlogger")
LOG_FILENAME = "EW.log"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
SERVER_PORT = 12345
SERVER_HOST = '192.168.1.104'

def main(host: str, port: int, log_level):
	print("World server started")
	logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT, filemode="w", level=log_level)
	logging.info('World server started')

	server_configuration = utils.get_config('server')
	if server_configuration is not None:
		host = server_configuration['host']
		port = server_configuration['port']

	world_configuration = utils.get_config('world')
	if world_configuration is None:
		logging.error(f"World configuration is missing in file 'server.json'")
		print("World server stopped due to error. Check {LOG_FILENAME}")
		exit ()
	
	world = TWorld(world_configuration['name'])
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
	try:
		host = utils.get_local_ip()
	except: 
		host = SERVER_HOST
	
	try:
		public_ip = utils.get_public_ip()
	except:
		pass
	
	log_level = logging.INFO
	try:
		if len(sys.argv) >= 2:
			host = sys.argv[1]
		if len(sys.argv) >= 3:
			port = int(sys.argv[2])
		if len(sys.argv) == 4:
			log_level = logging.DEBUG
		if len(sys.argv) > 4:
			raise SystemError()
	except:
		print(f"Usage: {sys.argv[0]} <host> <port> <log_level>")
		print(f"  <host> default value is {SERVER_HOST}")
		print(f"  <port> default value is {SERVER_PORT}")
		print(f"  <log_level> may be DEBUG")
		sys.exit(1)

	main(host, port, log_level)