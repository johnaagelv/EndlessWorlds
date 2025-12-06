from __future__ import annotations
#from server.worlds import TWorld
from worlds.world import TWorld

def cmd_fos(request: dict, world: TWorld) -> dict:
	world.actors[request["cid"]] = {
		"x": int(request["x"]),
		"y": int(request["y"]),
		"m": int(request["m"]),
		"face": request["face"],
	}

	response = world.get_map_field_of_sense(request['m'], request['x'], request['y'], request['r'])
	response["cid"] = request["cid"]
	response["cmd"] = request["cmd"]
	return response
