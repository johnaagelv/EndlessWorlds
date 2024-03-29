#!/usr/bin/env python3
import sys
import socket
import selectors
import traceback

from message import TMessage

sel = selectors.DefaultSelector()

def create_request(action: str = "fos"):
	if action == "fos":
		return dict(
			type="text/json",
			encoding="utf-8",
			content=dict(
				cmd = "fos",
				x =  3,
				y = 3,
				z = 0,
				r = 3,
#				i = "ABC-DEF-GHI-JKL"
			)
		)
	else:
		return dict(
			type="binary/custom-client-binary-type",
			encoding="binary",
			content=bytes(action + "value", encoding="utf-8"),
		)

def start_connection(host, port, request):
	addr = (host, port)
	print(f"Starting connection to {addr}")
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setblocking(False)
	sock.connect_ex(addr)
	events = selectors.EVENT_READ | selectors.EVENT_WRITE
	message = TMessage(sel, sock, addr, request)
	sel.register(sock, events, data=message)

def main():
	print("Start client")
	host, port = "192.168.1.106", 54321
	request = create_request()
	start_connection(host, port, request)

	try:
		while True:
			events = sel.select(timeout=1)
			for key, mask in events:
				message: TMessage = key.data
				try:
					data = message.process_events(mask)
					if data is not None:
						print(f"{data!r}")
				except Exception:
					print(
						f"Main: Error: Exception for {message.addr}:\n"
						f"{traceback.format_exc()}"
					)
					message.close()
			# Check for a socket being monitored to continue.
			if not sel.get_map():
				break
	except KeyboardInterrupt:
		print("Caught keyboard interrupt, exiting")
	finally:
		sel.close()

	print("Stop client")

if __name__ == "__main__":
	main()