from __future__ import annotations

from typing import Dict
import socket
import json
import requests
import logging
logger = logging.getLogger("EWlogger")

def get_local_ip() -> str:
	logger.info("get_local_ip()")
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()
	logger.debug(f"- ip = {ip}")
	return ip

def get_public_ip() -> str:
	logger.info("get_public_ip()")
	response = requests.get('https://api.ipify.org?format=json')
	ip = response.json()['ip']
	logger.debug(f"- ip = {ip}")
	return ip

def get_config(key: str) -> Dict:
	logger.info(f"get_config({key})")
	with open("server.json", "r") as f:
		data = json.load(f)
	try:
		value = data[key]
	except Exception:
		logger.warning(f"Configuration key {key!r} not found in file 'server.json'")
		value: dict = {}
	return value
