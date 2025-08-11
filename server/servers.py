from __future__ import annotations

import socket
import selectors
import traceback

from server_messages import TMessage
from worlds import TWorld

import logging
logger = logging.getLogger("EWlogger")

"""
Server 
"""
class TServer:
	def __init__(self, host: str, port: int, world: TWorld):
		logger.debug(f"TServer->init(host={host}, port={port})")
		print(f"- using {host}:{port}")
		self.host = host
		self.port = port
		self.world = world
		self.sel = selectors.DefaultSelector()
		lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Avoid bind() exception: OSError: [Errno 48] Address already in use
		lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		lsock.bind((self.host, self.port))
		lsock.listen()
		lsock.setblocking(False)
		self.sel.register(lsock, selectors.EVENT_READ, data=None)

	def accept_wrapper(self, sock: socket.socket):
		conn, addr = sock.accept()
		logger.debug(f"TServer->accept_wrapper(addr={addr})")
		conn.setblocking(False)
		message = TMessage(self.sel, conn, addr, self.world)
		self.sel.register(conn, selectors.EVENT_READ, data=message)

	def run(self):
		logger.debug("TServer->run()")
		loggerEventTypes = ['EVENT_UNKNOWN','EVENT_READ','EVENT_WRITE']
		events = self.sel.select(timeout=None)
		for key, mask in events:
			logger.debug(f"-> {loggerEventTypes[mask]}")
			if key.data is None:
				self.accept_wrapper(key.fileobj) # type: ignore
			else:
				# Client connection established, so get and process the message
				message: TMessage = key.data
				try:
					ready = message.dispatch(mask)
				except Exception:
					logger.warning(
						f"Main: Error: Exception for {message.addr}:\n"
						f"{traceback.format_exc()}"
					)
					message.close()

	def close(self):
		logger.debug("TServer->close()")
		self.sel.close()
