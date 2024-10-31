#!/usr/bin/env python3
import socket
import pickle
import uuid

from typing import Dict

HOST = "192.168.1.104"
PORT = 65432

def main() -> None:
	clients = dict()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
		server.bind((HOST, PORT))
		server.listen()

		while True:
			client_connection, addr = server.accept()
			with client_connection:
				print(f"Connected to {addr}")
				while True:
					data = client_connection.recv(1024)
					if not data:
						break
					command = pickle.loads(data)

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

						elif command["c"] == "mov":
							# Get the FOV at the x and y coordinate
							# Return the FOV
							result["c"] = "fov"
							result["a"] = [0,8,0]

						else:
							result["c"] = "nop"
					else:
						result["c"] = "nop"

					data = pickle.dumps(result)

					client_connection.sendall(data)

if __name__ == "__main__":
	main()