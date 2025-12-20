from __future__ import annotations
#from server.worlds import TWorld
from server.world import TWorld

def cmd_fos(request: dict, world: TWorld) -> dict:
	world.actors[request["cid"]] |= request

	response = world.get_map_field_of_sense(request['m'], request['x'], request['y'], request['r'])
	response["cid"] = request["cid"]
	response["cmd"] = request["cmd"]
	return response
