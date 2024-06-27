#!/usr/bin/env python3
import sys
import socket
import selectors
import traceback

from message import TMessage
from external_ip import get_ip

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
	print(f"- Initializing socket")
	sock.setblocking(False)
	print(f"- blocking false")
	sock.bind(("0.0.0.0",12345))
	print(f"- bound port 12345")
	sock.connect_ex(addr)
	print(f"- connected")
	events = selectors.EVENT_READ | selectors.EVENT_WRITE
	message = TMessage(sel, sock, addr, request)
	sel.register(sock, events, data=message)
	print(f"- register socket with selector")

def main():
	print("Start client")
	ip = get_ip(local = True)
#	ip = "endlessworlds.hopto.org"
	port = 54321
	request = create_request()
	start_connection(ip, port, request)

	try:
		print("Starting loop")
		while True:
			print("- waiting for event")
			events = sel.select(timeout=5)
			print(f"- processing events {events!r}")
			for key, mask in events:
				print("- getting message instance")
				message: TMessage = key.data
				try:
					print("- try message processing")
					data = message.process_events(mask)
					if data is not None:
						print(f"{data!r}")
				except Exception:
					print(
						f"Main: Error: Exception for {message.addr}:\n"
						f"{traceback.format_exc()}"
					)
					message.close()
			print("- events processed")
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