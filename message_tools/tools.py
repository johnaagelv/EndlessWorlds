from __future__ import annotations
from collections.abc import Callable

import message_tools.json_packager as json_packager
import message_tools.binary_packager as binary_packager

# Define the command handler interface
type packageFn = Callable[[dict], bytes]

# Registry of command handlers
message_packager: dict[str, packageFn] = {
	"json": json_packager.generate_json_message,
	"binary": binary_packager.generate_binary_message,
}

"""
Generate the message
"""
def generate_message(message_type: str, message: dict) -> bytes:
	#logger.debug("generate_message( message_type, message )")
	packager = message_packager.get(message_type)
	if packager:
		return packager(message)
	return b""
