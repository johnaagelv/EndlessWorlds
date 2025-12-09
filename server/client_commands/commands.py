from __future__ import annotations

from collections.abc import Callable

import server.client_commands.new as new
import server.client_commands.fos as fos

from server.world import TWorld

# Define the command handler interface
type commandFn = Callable[[dict, TWorld], dict]

# Registry of command handlers
client_commands: dict[str, commandFn] = {
	"new": new.cmd_new,
	"fos": fos.cmd_fos,
}
