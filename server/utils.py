from typing import Dict
import socket
import json
import logging
logger = logging.getLogger("EWlogger")
def get_local_ip() -> str:
	logger.debug("get_local_ip()")
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()
	return ip

def get_public_ip() -> str:
	logger.debug("get_public_ip()")
	import requests
	response = requests.get('https://api.ipify.org?format=json')
	ip = response.json()['ip']
	return ip

def get_config(key: str) -> Dict:
	logger.debug(f"get_config({key})")
	with open("server/server.json", "r") as f:
		data = json.load(f)
	try:
		value = data[key]
	except Exception as e:
		logger.warning(f"Configuration key {key!r} not found in file 'server.json'")
		value = None
	return value