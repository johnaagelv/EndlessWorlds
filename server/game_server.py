from __future__ import annotations

import socket
import selectors
import traceback

from connection_handler import TConnectionHandler #, TSender
from worlds import TWorld

import logging

from collections.abc import Callable
from client_commands import new, fos
type commandFn = Callable[[dict, TWorld], dict]

# Registry of client commands
client_commands: dict[str, commandFn] = {
	"new": new.cmd_new,
	"fos": fos.cmd_fos
}

logger = logging.getLogger("EWlogger")

"""
Game server - handles all connections between client and server
"""
host: str
port: int
sel = selectors.DefaultSelector()

def init(server_host: str, server_port: int):
	host = server_host
	port = server_port
	lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	lsock.bind((host, port))
	lsock.listen()
	lsock.setblocking(False)
	sel.register(lsock, selectors.EVENT_READ, data=None)

"""
Establish connection handler for a client
"""
def accept_wrapper(sock: socket.socket):
	logger.debug("TServer->accept_wrapper( sock )")
	# Accept a connection from a client
	client_connection: socket.socket
	client_address: str
	client_connection, client_address = sock.accept()
	# Make sure the connection does not block
	client_connection.setblocking(False)
	# Initiate the message handler for this client connection
	client_communicator = TConnectionHandler(sel, client_connection, client_address)
	# start monitoring the client connection for events
	sel.register(client_connection, selectors.EVENT_READ, data=client_communicator)

"""
Process events
"""
def run(world: TWorld):
	logger.debug("TServer->run()")
	loggerEventTypes = ['EVENT_UNKNOWN','EVENT_READ','EVENT_WRITE']
	# Get any events received by the game server
	events = sel.select(timeout=None)
	for key, mask in events:
		logger.debug(f"-> {loggerEventTypes[mask]}")
		if key.data is None:
			accept_wrapper(key.fileobj) # type: ignore
		else:
			# Client connection established, so get and process the message
			client_communicator: TConnectionHandler = key.data
			try:
				if mask == selectors.EVENT_READ:
					# Has a request been received?
					if client_communicator.dispatch(mask):
						# Get the client command processor
						client_command = client_commands.get(client_communicator.request["cmd"])
						# Set default response if no client command processor found
						response: dict = {}
						if client_command is not None:
							# Process the request
							response = client_command(client_communicator.request, world)

						client_communicator.prepare_response(response)
				else:
					# Has the response been sent?
					if client_communicator.dispatch(mask):
						# End of communication with the client
						client_communicator.close()
					
			except Exception:
				logger.warning(
					f"Main: Error: Exception for {client_communicator.addr}:\n"
					f"{traceback.format_exc()}"
				)
				client_communicator.close()

def close():
	logger.debug("TServer->close()")
	sel.close()
