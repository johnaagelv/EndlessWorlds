from __future__ import annotations
from server.world import TWorld

def cmd_nop(request: dict, world: TWorld) -> dict:
	response: dict = {"cmd": "nop"}
	return response
