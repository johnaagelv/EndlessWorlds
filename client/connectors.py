from typing import Any, Dict
import types
import selectors
import socket
import pickle

from messages import TClientMessage

class TConnector:
	"""
	Initialize the connection to a HUB server
	"""
	def __init__(self, host: str, port: int):
		self.host = host
		self.port = port
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect((self.host, self.port))
		self.client.setblocking(False)
		self.sel = selectors.DefaultSelector()
		self.sel.register(self.client, selectors.EVENT_READ | selectors.EVENT_WRITE, data=None)

	def execute(self, request: Dict) -> Dict:
		message = TClientMessage(self.sel, self.client, (self.host, self.port), request)
		self.sel.modify(self.client, selectors.EVENT_READ | selectors.EVENT_WRITE, data=message)
		while True:
			events = self.sel.select()
			for key, mask in events:
				message: TClientMessage = key.data
				try:
					message.process_events(mask)
				except Exception:
					pass
					message.close()
			if not self.sel.get_map():
				break

		print(f"Message result: {message.response}")
#		return message.response
