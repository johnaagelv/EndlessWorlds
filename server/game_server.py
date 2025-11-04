from __future__ import annotations

import socket
import selectors
import traceback

from server.connection_handler import TConnectionHandler #, TSender
from server.worlds import TWorld

from message_packages.packages import message_packager

import logging

#from collections.abc import Callable
from client_commands.commands import client_commands

logger = logging.getLogger("EWlogger")

"""
Generate the message
"""
def generate_message(message_type: str, message: dict) -> bytes:
	logger.debug("generate_message( message_type, message )")
	packager = message_packager.get(message_type)
	if packager:
		return packager(message)
	return b""

"""
Game server - handles all connections between client and server
"""
host: str
port: int
server_selector = selectors.DefaultSelector()
server_socket: socket.socket

def init(server_host: str, server_port: int):
	host = server_host
	port = server_port
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# Binds address to the socket. The address contains the pair of hostname and the port number.
	server_socket.bind((host, port))
	# Starts the TCP listener
	server_socket.listen()
	server_socket.setblocking(False)
	# Start the selector event handler for read events from the server socket
	server_selector.register(server_socket, selectors.EVENT_READ, data=None)

"""
Accept a connection
- establish a connection handler for the connection
- register the connection and the connection handler with the server selector
"""
def accept_wrapper(event_socket: socket.socket):
	logger.debug("server->accept_wrapper( event_socket )")
	# Passively accepts the TCP client connection
	client_connection, client_address = event_socket.accept()
	logger.debug(f"- client {client_address}")
	# Make sure the connection does not block
	client_connection.setblocking(False)
	# Initiate the message handler for this client connection
	connection_handler = TConnectionHandler(server_selector, client_connection, client_address)
	# start monitoring the client connection for read events
	server_selector.register(client_connection, selectors.EVENT_READ, data=connection_handler)

"""
Process events
"""
def run(world: TWorld):
	logger.debug("server->run( world )")
	loggerEventTypes = ['EVENT_UNKNOWN','EVENT_READ','EVENT_WRITE']
	# Get any events received by the game server
	events = server_selector.select(timeout=None)
	for key, mask in events:
		logger.debug(f"-> {loggerEventTypes[mask]}")
		if key.data is None:
			accept_wrapper(key.fileobj) # type: ignore
		else:
			# Client connection established, so get and process the message
			client_communicator: TConnectionHandler = key.data
			try:
				if mask == selectors.EVENT_READ:
					# Has a message been received?
					if client_communicator.dispatch(mask):
						# Get the client command processor
						command_handler = client_commands.get(client_communicator.message["cmd"])

						if command_handler is not None:
							# Process the message
							client_communicator._buffer = generate_message(
								message_type = "binary",
								message = command_handler(client_communicator.message, world)
							)
							client_communicator.prepare_to_send()
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
	logger.debug("server->close()")
	server_selector.close()
