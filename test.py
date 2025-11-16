#!/usr/bin/env python3
import random
import selectors
import socket

from connections.connection_handler import TConnectionHandler
from message_tools.tools import generate_message

import logging
logger = logging.getLogger("EWlogger")
LOG_FILENAME = "EWtester.log"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT, filemode="w", level=logging.DEBUG)

hostname = socket.gethostname()

HOST = "192.168.1.104"  # The server's hostname or IP address
PORT = 25261  # The port used by the server

host = HOST
port = PORT
sel = selectors.DefaultSelector()

"""
Establish connection handler to the server
"""
def start_connection(request: dict, request_type: dict):
	logger.debug("start_connection( request, request_type )")
	# Accept a connection from a client
	client_connection: socket.socket
	client_address = (host, port)
	client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Make sure the connection does not block
	client_connection.setblocking(False)
	client_connection.connect_ex(client_address)
	# Initiate the message handler for this client connection
	client_communicator = TConnectionHandler(sel, client_connection, host+":"+str(port))
#	client_communicator.prepare_to_send(request, request_type)
	client_communicator._buffer = generate_message(
		message_type = "binary",
		message = request
	)

	# start monitoring the client connection for events
	sel.register(client_connection, selectors.EVENT_WRITE, data=client_communicator)

def run() -> bool:
	events = sel.select()
	for key, mask in events:
		if key.data is not None:
			client_communicator: TConnectionHandler = key.data
			try:
				if mask == selectors.EVENT_READ:
					# Has a request been received?
					if client_communicator.dispatch(mask):
						result = client_communicator.message['cmd']
						logger.debug(f"- response received ... {result}")
						# Message has been received, return False to stop
						return False
				else:
					# Has the response been sent?
					if client_communicator.dispatch(mask):
						logger.debug("- message sent ...")
						client_communicator.message = {}
#						logger.debug("- message cleared")
						client_communicator._jsonheader_len = -1
						client_communicator.jsonheader = {}

						client_communicator._set_selector_events_mask("r")
					
			except Exception:
				logger.error(
					f"Main: Error: Exception for {client_communicator.addr}:"
				)
				client_communicator.close()
	return True

def close():
	sel.close()

def main():
	print("Client started")

	request = {
		"cmd":"new",
		"cid": "1234", # if CID is not provided, then this is a new actor and will be placed in the world by the server
		"m": 0,
		"x": 10,
		"y": 10,
		"z": 0,
		"r": random.randint(2,8),
	}
	request_type: dict = {"content-type": "binary/binary"}
	logger.debug("- starting connection ...")
	start_connection(request, request_type)

	request = {
		"cmd":"fos",
		"cid": "1234", # if CID is not provided, then this is a new actor and will be placed in the world by the server
		"m": 0,
		"x": 10,
		"y": 10,
		"z": 0,
		"r": random.randint(2,8),
	}

	logger.debug("- running ...")

#	while True:

	while run():
		pass
		
#		time.sleep(10.0)

	start_connection(request, request_type)
	while run():
		pass

	print("Client stopped")

if __name__ == "__main__":
	main()