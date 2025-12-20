from __future__ import annotations

from server.world import TWorld

def cmd_get(request: dict, world: TWorld) -> dict:
	response = request
	items = [(idx, item) for idx, item in enumerate(world.maps[request["m"]]["items"]) if item["iid"] == request["iid"]]
	if len(items) > 0:
		del(world.maps[request["m"]]["items"][items[0][0]])
	else:
		response["iid"] = ""
	return response