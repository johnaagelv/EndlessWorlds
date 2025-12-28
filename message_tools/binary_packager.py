from __future__ import annotations

import json
import sys
import struct
import pickle
import logging
logger = logging.getLogger("EWlogger")

"""
Generate a binary header dictionary
"""
def generate_binary_message(data: dict) -> bytes:
	logger.debug("generate_binary_message")
	content_bytes = pickle.dumps(data)
	jsonheader = {
		"byteorder": sys.byteorder,
		"content-type": "binary/custom-server-binary-type",
		"content-encoding": "binary",
		"content-length": len(content_bytes),
	}
	jsonheader_bytes = json.dumps(jsonheader, ensure_ascii=False).encode("utf-8")
	message_hdr = struct.pack(">H", len(jsonheader_bytes))
	logger.debug("- generated")
	return message_hdr + jsonheader_bytes + content_bytes
