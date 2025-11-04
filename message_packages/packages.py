from __future__ import annotations
from collections.abc import Callable

import message_packages.json as json
import message_packages.binary as binary

# Define the command handler interface
type packageFn = Callable[[dict], bytes]

# Registry of command handlers
message_packager: dict[str, packageFn] = {
	"json": json.generate_json_message,
	"binary": binary.generate_binary_message,
}

