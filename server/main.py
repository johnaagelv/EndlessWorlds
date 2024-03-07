#!/usr/bin/env python3

import sys
import selectors, socket

from world import TWorld
from world_server import TServer

"""
Accept connections from clients
"""
def shutdown(self):
	pass

def main(name: str):
	world = TWorld(name=name)
	ip = "192.168.1.106"
	port = 54321
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