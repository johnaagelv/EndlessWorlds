#!/usr/bin/env python3
import socket
import selectors
import types

import pickle
import uuid

from typing import Dict

from game_map import TGameMap
from procgen import generate_dungeon

HOST = "192.168.1.104"
PORT = 65432

sel = selectors.DefaultSelector()
clients = dict()

def service_connection(key, mask, game_map):
	sock = key.fileobj
	data = key.data
	if mask & selectors.EVENT_READ:
		recv_data = sock.recv(1024)
		if recv_data:
			command = pickle.loads(recv_data)
			result = command
			if "c" in command.keys():
				if command["c"] == "connect":
					# Establish client connection
					if "i" in command.keys():
						if command["i"] in clients.keys():
							pass
						else:
							clients[command["i"]] = command["i"]
					else:
						client = uuid.uuid1()
						clients[client] = client
						result["i"] = client
						# return the map size
						result["w"] = 80
						result["h"] = 45

				elif command["c"] == "mov":
					# Get the FOV at the x and y coordinate
					# Return the FOV
					result["c"] = "fov"
					result["a"] = [0,8,0]

				else:
					result["c"] = "nop"
			else:
				result["c"] = "nop"

			data.outb = pickle.dumps(result)
		else:
			sel.unregister(sock)
			sock.close()
	if mask & selectors.EVENT_WRITE:
		if data.outb:
			sent = sock.send(data.outb)
			data.outb = data.outb[sent:]

def accept_wrapper(client_socket):
	client_connection, addr = client_socket.accept()
	client_connection.setblocking(False)
	data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
	events = selectors.EVENT_READ | selectors.EVENT_WRITE
	sel.register(client_connection, events, data=data)

def main() -> None:

	game_map = generate_dungeon(80, 45)

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
		server.bind((HOST, PORT))
		server.listen()
		server.setblocking(False)
		sel.register(server, selectors.EVENT_READ, data=None)

		while True:
			events = sel.select(timeout = None)

			for key, mask in events:
				if key.data is None:
					accept_wrapper(key.fileobj)
				else:
					service_connection(key, mask, game_map)
	
	
if __name__ == "__main__":
	main()