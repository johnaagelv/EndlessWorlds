import socket
import selectors
import traceback

from server_messages import TMessage
from worlds import TWorld

"""
Server 
"""
class TServer:
	def __init__(self, host: str, port: int, world: TWorld):
		print(f"TServer->init(host={host}, port={port})")
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
		print(f"TServer->accept_wrapper(addr={addr})")
		conn.setblocking(False)
		message = TMessage(self.sel, conn, addr, self.world)
		self.sel.register(conn, selectors.EVENT_READ, data=message)

	def run(self):
		print(f"TServer->run()")
		events = self.sel.select(timeout=None)
		for key, mask in events:
			if key.data is None:
				self.accept_wrapper(key.fileobj)
			else:
				# Client connection established, so get and process the message
				message: TMessage = key.data
				try:
					message.dispatch(mask)
				except Exception:
					print(
						f"Main: Error: Exception for {message.addr}:\n"
						f"{traceback.format_exc()}"
					)
					message.close()

	def close(self):
		print(f"TServer->close()")
		self.sel.close()
