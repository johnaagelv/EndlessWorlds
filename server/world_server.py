import selectors, socket, traceback

from world import TWorld
class TMessage:
	def __init__(self, sel: selectors.BaseSelector, conn, addr):
		self.sel = sel
		self.conn = conn
		self.addr = addr

	def process_events(self, mask):
		pass

class TServer:
	def __init__(self, ip: str, port: int):
		self.is_running = True
		self.ip = ip
		self.port = port
		self.is_running = True

	def accept(self):
		conn, addr = self.sock.accept()  # Should be ready to read
		# print(f"- {addr}")
		conn.setblocking(False)
		message = TMessage(self.sel, conn, addr)
		self.sel.register(conn, selectors.EVENT_READ, data=message)

	def startup(self):
		print(f"TServer->startup()")
		# Using the default selector
		self.sel = selectors.DefaultSelector()
		# Set up a socket for network connection
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Avoid bind() exception: OSError: [Errno 48] Address already in use
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.ip, self.port))
		self.sock.listen()
		self.sock.setblocking(False)
		self.sel.register(self.sock, selectors.EVENT_READ, data=None)

	def run(self, world: TWorld):
		print(f"TServer->run(world)")
		try:
			while self.is_running:
				events = self.sel.select(timeout=None)
				for key, mask in events:
					print(f"key={key}, mask={mask}")
					if key.data is None:
						self.accept_wrapper(key.fileobj)
					else:
						message: TMessage = key.data
						try:
							message.world = world
							message.process_events(mask)
						except Exception:
							print(
								f"Server: Error: Exception for {message.addr}:\n"
								f"{traceback.format_exc()}"
							)
							message.close()
		except KeyboardInterrupt:
			pass
			# print("Caught keyboard interrupt, exiting")
		finally:
			self.sel.close()

	def shutdown(self):
		print(f"TServer->shutdown")
