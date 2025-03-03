import socket
def get_local_ip() -> str:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()
	return ip

def get_public_ip() -> str:
	import requests
	response = requests.get('https://api.ipify.org?format=json')
	ip = response.json()['ip']
	return ip
