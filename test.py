#!/usr/bin/env python3
import json
import socket
import struct
import sys
import random

from typing import Tuple
import numpy as np

hostname = socket.gethostname()
print(hostname)
print(socket.gethostbyname(hostname))

graphic_dt = np.dtype(
	[
		("ch", np.int32), # Unicode codepoint
		("fg", "3B"), # 3 unsigned bytes, foreground RGB colours
		("bg", "3B"), # Background RGB colours
	]
)

tile_dt = np.dtype(
	[
		("walkable", bool), # True if walkable tile
		("transparent", bool), # True if tile doesn't block FOV
		("dark", graphic_dt), # Graphics outside of FOV
		("light", graphic_dt), # Graphics inside of FOV
	]
)

def new_tile(
	*,
	walkable: int,
	transparent: int,
	dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
	light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
	return np.array((walkable, transparent, dark, light), dtype=tile_dt)

floor = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord(" "), (255, 255, 255), (96, 64, 64)),
	light=(ord(" "), (255, 255, 255), (128, 96, 96)),
)

wall = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord("#"), (255, 255, 255), (32, 32, 32)),
	light=(ord("#"), (255, 255, 255), (64, 64, 64)),
)

HOST = "192.168.1.104"  # The server's hostname or IP address
PORT = 12345  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))

	command = {
		"cmd":"fos",
		"cid": 0, # must always be provided
		"m": 0,
		"x": 10,
		"y": 10,
		"z": 0,
		"r": random.randint(2,8),
	}

	command = {
		"cmd":"new", # if CID is not provided, then this is a new actor and will be placed in the world by the server
	}

	data = json.dumps(command, ensure_ascii=False).encode('utf-8')

	jsonheader = {
		"byteorder": sys.byteorder,
		"content-type": "text/json",
		"content-encoding": "utf-8",
		"content-length": len(data),
	}
	jsonheader_bytes = json.dumps(jsonheader, ensure_ascii=False).encode("utf-8")
	message_hdr = struct.pack(">H", len(jsonheader_bytes))
	message = message_hdr + jsonheader_bytes + data

	s.sendall(message)
	message = b""
	r = True
	print("Receiving ...")
	while r:
		data = s.recv(65536)
		if data:
			print(f"- received {len(data)} bytes")
			message += data
		else:
			r = False
	
	print(message)
	s.close()
