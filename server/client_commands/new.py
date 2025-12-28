from __future__ import annotations
import uuid
import random
from server.world import TWorld
import logging
logger = logging.getLogger("EWlogger")

def cmd_new(request: dict, world: TWorld) -> dict:
	logger.debug(f"cmd_new( {request}, world )")
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
		entry_points = world.get_world_entry_points()

		response["entry_point"] = entry_points[random.randint(0,len(entry_points)-1)]

	world.actors[response["cid"]] = {
		"x": int(response["entry_point"][0]),
		"y": int(response["entry_point"][1]),
		"z": int(response["entry_point"][2]),
		"m": int(response["entry_point"][3]),
		"face": request["face"],
		"skin": request["skin"], # skin colour of the actor
	}

	response["name"] = world.name
	response["map_sizes"] = world.get_world_definition()
	return response
