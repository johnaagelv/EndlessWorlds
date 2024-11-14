#!/usr/bin/env python3

HOST = "192.168.1.104"
PORT = 65432

MAP_WIDTH = 80
MAP_HEIGHT = 45

from servers import TServer

def main():
	server = TServer(HOST, PORT)
	server.run()
	
if __name__ == "__main__":
	main()