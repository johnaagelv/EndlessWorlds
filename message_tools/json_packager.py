from __future__ import annotations

import sys
import struct
import json
import logging
logger = logging.getLogger("EWlogger")

"""
Generate a json message
"""
def generate_json_message(data: dict) -> bytes:
	content_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
	jsonheader = {
		"byteorder": sys.byteorder,
		"content-type": "text/json",
		"content-encoding": "utf-8",
		"content-length": len(content_bytes),
	}
	jsonheader_bytes = json.dumps(jsonheader, ensure_ascii=False).encode("utf-8")
	message_hdr = struct.pack(">H", len(jsonheader_bytes))
	return message_hdr + jsonheader_bytes + content_bytes
