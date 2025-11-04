from __future__ import annotations

import json
import struct
import sys
import logging
from message_packages.packages import message_packager

logger = logging.getLogger("EWlogger")

"""
Construct a message from the specified data elements
"""
def create_message(*, content_bytes: bytes, content_type: str, content_encoding: str):
	logger.debug("create_message( *, content_bytes, content_type, content_encoding )")
	jsonheader = {
		"byteorder": sys.byteorder,
		"content-type": content_type,
		"content-encoding": content_encoding,
		"content-length": len(content_bytes),
	}
	jsonheader_bytes = json_encode(jsonheader, "utf-8")
	message_hdr = struct.pack(">H", len(jsonheader_bytes))
	message = message_hdr + jsonheader_bytes + content_bytes
	return message

"""
Generate the message
"""
def generate_message(self, message_type: str):
	logger.debug(f"{__class__.__name__}->generate_message( message_type, message )")
	packager = message_packager.get(message_type)
	if packager:
		message_package = packager(self.message)

		logger.debug(f"- package {message_package}")
		return create_message(**message_package) # ** is unpacking the dictonary to the method
