from __future__ import annotations
from worlds import TWorld

def cmd_fos(request: dict, world: TWorld) -> dict:
	response = world.field_of_sense(request, False)
	response["cid"] = request["cid"]
	response["cmd"] = request["cmd"]
	return response
