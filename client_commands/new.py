from __future__ import annotations
import uuid
from server.worlds import TWorld

def cmd_new(request: dict, world: TWorld) -> dict:
	cmd_keys = request.keys()
	response: dict = {"cmd": "new"}
	if "cid" in cmd_keys:
		response["cid"] = request["cid"]
		response["entry_point"] = [
			request["x"],
			request["y"],
			request["z"],
			request["m"]
		]
	else:
		response["cid"] = uuid.uuid4()
		response["entry_point"] = world.entry_point()

	world.actors[response["cid"]] = {
		"x": response["entry_point"][0],
		"y": response["entry_point"][1],
		"z": response["entry_point"][2],
		"m": response["entry_point"][3]
	}

	response["name"] = world.name
	response["map_sizes"] = world.map_definitions()
	return response
