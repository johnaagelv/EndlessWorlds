""" Get the local or the public IP address """
import socket

ExternalDNS = "8.8.8.8"
ExternalURL = "endlessworlds.hopto.org"

def get_ip(local: bool = True) -> str:
	if local: # Get local IP address
		try:
			ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect((ExternalDNS, 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
		except Exception:
			ip = "127.0.0.1"

	else: # Get public IP address
		print("Get public address")
		try:
			ip = socket.gethostbyname(ExternalURL)
		except Exception:
			print("- public is localhost")
			ip = "127.0.0.1"

	return ip