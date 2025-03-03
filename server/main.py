#!/usr/bin/env python3
import sys

import utils

from servers import TServer
from worlds import TWorld

SERVER_PORT = 12345
SERVER_HOST = '192.168.1.104'

def main(host: str, port: int):
	world = TWorld()
	server = TServer(host, port, world)
	try:
		while True:
			server.run()

	except KeyboardInterrupt:
		server.sel.close()
		print(f"Server closed!")

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
	
	try:
		if len(sys.argv) >= 2:
			host = sys.argv[1]
		if len(sys.argv) == 3:
			port = int(sys.argv[2])
		if len(sys.argv) > 3:
			raise SystemError()
	except:
		print(f"Usage: {sys.argv[0]} <host> <port>")
		print(f"  <host> default value is {SERVER_HOST}")
		print(f"  <port> default value is {SERVER_PORT}")
		sys.exit(1)

	main(host, port)