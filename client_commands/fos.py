from __future__ import annotations
from server.worlds import TWorld

def cmd_fos(request: dict, world: TWorld) -> dict:
	response = world.field_of_sense(request, False)
	response['actors'] = world.fos_actors(request)
	response["cid"] = request["cid"]
	response["cmd"] = request["cmd"]
	return response
