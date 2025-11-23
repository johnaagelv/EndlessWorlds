from __future__ import annotations
from worlds import TWorld

def cmd_nop(request: dict, world: TWorld) -> dict:
	response: dict = {"cmd": "nop"}
	return response
