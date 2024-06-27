#!/usr/bin/env python3

import sys

from world import TWorld
from world_server import TServer
from external_ip import get_ip


"""
Accept connections from clients
"""
def shutdown(self):
	pass

def main(name: str):
	ip = get_ip(local=True) # Get the local IP address for the server
	port = 54321

	world = TWorld(name=name)
	
	server = TServer(ip=ip, port=port)

	server.startup()
	server.run(world=world)
	server.shutdown()

if __name__ == "__main__":
	if len(sys.argv) == 2:
		name = sys.argv[1]
	else:
		name = "demo"
	main(name=name)