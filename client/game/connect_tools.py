from __future__ import annotations

import socket
import selectors
import struct
import sys
import pickle
import json

import client.g as g
from connections.connection_handler import TConnectionHandler

import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

"""
Generate a binary header dictionary
"""
def generate_binary_message(data: dict) -> bytes:
#	logger.debug("generate_binary_message")
	content_bytes = pickle.dumps(data)
	jsonheader = {
		"byteorder": sys.byteorder,
		"content-type": "binary/custom-server-binary-type",
		"content-encoding": "binary",
		"content-length": len(content_bytes),
	}
	jsonheader_bytes = json.dumps(jsonheader, ensure_ascii=False).encode("utf-8")
	message_hdr = struct.pack(">H", len(jsonheader_bytes))
	return message_hdr + jsonheader_bytes + content_bytes

def start_connection(request: dict):
#	logger.debug("start_connection( request )")
	# Accept a connection from a client
	host = "192.168.1.104"
	port = 25261
	client_connection: socket.socket
	client_address = (host, port)
	client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Make sure the connection does not block
	client_connection.setblocking(False)
	client_connection.connect_ex(client_address)
	# Initiate the message handler for this client connection
	client_communicator = TConnectionHandler(g.sel, client_connection, host+":"+str(port))
#	client_communicator.prepare_to_send(request, request_type)
	client_communicator._buffer = generate_binary_message(request)
	# start monitoring the client connection for events
	g.sel.register(client_connection, selectors.EVENT_WRITE, data=client_communicator)

def query_server(request: dict) -> dict:
#	logger.debug(" ")
#	logger.debug(f"query_server( request {request['cmd']})")
	start_connection(request)
	query_on = True
	result: dict = {}
	while query_on:
		events = g.sel.select()
		for key, mask in events:
			if key.data is not None:
				client_communicator: TConnectionHandler = key.data
				try:
					if mask == selectors.EVENT_READ:
						# Has a request been received?
						if client_communicator.dispatch(mask):
							result = client_communicator.message
							logger.debug("- response received ...")
							logger.debug(result)
							# Message has been received, set False to stop
							query_on = False
					else:
						# Has the response been sent?
						if client_communicator.dispatch(mask):
#							logger.debug("- message sent ...")
							client_communicator.message = {}
							client_communicator._jsonheader_len = -1
							client_communicator.jsonheader = {}
							client_communicator._set_selector_events_mask("r")
						
				except Exception:
					logger.error(
						f"Main: Error: Exception for {client_communicator.addr}:"
					)
					client_communicator.close()
	return result