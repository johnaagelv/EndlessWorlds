from __future__ import annotations
#from server.worlds import TWorld
from server.world import TWorld
import logging
logger = logging.getLogger("EWlogger")

def cmd_fos(request: dict, world: TWorld) -> dict:
	logger.debug(f"cmd_fos( {request}, world )")
	world.actors[request["cid"]] |= request

	response = world.get_map_field_of_sense(request['m'], request['x'], request['y'], request['r'])
	response["cid"] = request["cid"]
	response["cmd"] = request["cmd"]
	return response
