import socket
import json

class TServer:
	def __init__(self):
		pass

	def send(self, data: str, host, port) -> str:
		client_socket = socket.socket()  # instantiate
		client_socket.connect((host, port))  # connect to the server
		data = bytes(json.dumps(data), 'utf-8')
		client_socket.send(data)  # send message
		data, ancdata, flags, addr = client_socket.recvmsg(4096)  # receive response
		client_socket.close()  # close the connection
		return json.loads(data.decode())
