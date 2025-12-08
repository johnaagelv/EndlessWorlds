from __future__ import annotations

import numpy as np

from random import Random, randint
from tcod.ecs import Registry
import community.tile_types as tile_types
import community.g as g
from community.game.components import CID, Graphic, IsPlaying, Maps, Name, Position, World, Vision, StateName, StateValue, StateMax, StateUsage
from community.game.tags import IsActor, IsPlayer, IsWorld

import community.game.connect_tools

import community.configuration as config
import community.ui.configuration as ui

def generate_name() -> str:
	wovels = "aeiouy"
	consonants = "bcdfghjklmnpqrstvwxz"
	rules = [
		[0,1,0,0,1,1,0],
		[0,1,1,0,1,0],
		[1,0,1,0],
		[1,0,0,1,1,0,1],
		[1,0,1,1],
		[1,0,0,1],
	]
	rule = rules[randint(0, len(rules)-1)]
	name: str = ""
	for rule_rule in rule:
		match rule_rule:
			case 0: # wovel
				name += wovels[randint(0, len(wovels)-1)]
			case 1: # consonant
				name += consonants[randint(0, len(consonants)-1)]
	print(name)	
	return name

def new_game(actor_count: int) -> Registry:
	game = Registry()
	rng = game[object()].components[Random] = Random()  # noqa: F841

	faces = [9786, 9787, 937, 38]

	world = game[object()]
	print(f"Generating {actor_count} NPCs")
	for i in range(0, actor_count):
		actor = game[object()]
		actor.components[Name] = generate_name()
		face = faces[rng.randint(0,len(faces) - 1)]
		result = community.game.connect_tools.query_server(
			{
				"cmd": "new",
				"face": face,
			}
		)
		if i == 0:
			map_sizes = result['map_sizes']
			map_template = {
				"loaded": bool,
				"width": int,
				"height": int,
				"tiles": np.ndarray,
				"visible": np.ndarray,
				"explored": np.ndarray,
				"gateways": list,
				"actors": list,
			}
			map_template["loaded"] = False
			world.components[World] = World()
			world.components[Maps] = Maps([map_template] * len(map_sizes), map_sizes)
			world.tags |= {IsWorld}
		
		actor.components[CID] = result["cid"]
		actor.components[Position] = Position(result['entry_point'][0], result['entry_point'][1], result['entry_point'][3])
		actor.components[Graphic] = Graphic(face, (randint(64,255),randint(64,255),randint(64,255)))
		actor.components[IsPlaying] = True
		actor.tags |= {IsPlayer, IsActor}
		actor.components[Vision] = rng.randint(6,16)
		for actor_state in config.ACTOR_STATES:
			actor.components[StateName] = actor_state[0]
			actor.components[StateValue] = actor_state[1]
			actor.components[StateMax] = actor_state[2]
			actor.components[StateUsage] = actor_state[3]

	return game

def start_map(map_idx: int) -> None:
	""" Start a map from the definition when it hasnt been loaded fully yet """
	(world,) = g.game.Q.all_of(tags=[IsWorld])
	maps = world.components[Maps]
	if not maps.maps[map_idx]['loaded']:
		definition = maps.defs[map_idx]
		map_width = int(definition["width"])
		map_height = int(definition["height"])
		map_visible = definition["visible"]
		maps.maps[map_idx] = {
			"loaded": True,
			"name": definition["name"],
			"width": map_width,
			"height": map_height,
			"gateways": definition["gateways"],
			"tiles": np.full((map_width, map_height), fill_value=tile_types.blank, order="F"),
			"visible": np.full((map_width, map_height), fill_value=map_visible, order="F"),
			"explored": np.full((map_width, map_height), fill_value=map_visible, order="F"),
		}

		if map_visible:
#			logger.debug(f"- visible map {map_idx}")
			fos: dict = definition["fos"]
			temp = fos.get("view")
			view = np.array(temp)
			maps.maps[map_idx]["tiles"][0:map_width, 0:map_height] = view

def in_gateway(x: int, y: int, map_idx: int) -> bool:
	""" Return true when the location has a gateway """
	(world,) = g.game.Q.all_of(tags=[IsWorld])
	maps = world.components[Maps]
	return maps.maps[map_idx]["tiles"][x, y]["gateway"]

def go_gateway(x: int, y: int, map_idx: int, direction = None) -> dict:
	""" Return the gateway at the current location """
	(world,) = g.game.Q.all_of(tags=[IsWorld])
	maps = world.components[Maps]
	gateway_fallback = {
		"gateway": {
			"x": x,
			"y": y,
			"m": map_idx,
			"h": ""
		}
	}
	if direction is None:
		gateway = next((item for item in maps.maps[map_idx]["gateways"] if item["x"] == x and item["y"] == y), gateway_fallback)
	else:
		gateway = next((item for item in maps.maps[map_idx]["gateways"] if item["x"] == x and item["y"] == y and item['action'] == direction), gateway_fallback)
	return gateway

def get_view_port(pos: Position) -> tuple:
	""" Calculate the view port """
	(world,) = g.game.Q.all_of(tags=[IsWorld])
	maps = world.components[Maps]

	view_width = ui.VIEW_PORT_WIDTH
	view_height = ui.VIEW_PORT_HEIGHT

	width = maps.maps[pos.m]["width"]
	height = maps.maps[pos.m]["height"]

	view_x1 = min(max(0, pos.x - int(view_width / 2)), width - view_width)
	view_x2 = view_x1 + view_width

	view_y1 = min(max(0, pos.y - int(view_height / 2)), height - view_height)
	view_y2 = view_y1 + view_height
	return (view_x1, view_x2, view_y1, view_y2)

#def get_entities_at_location(self, location_x: int, location_y: int) -> Optional[List]:
#	return [entity for entity in self.entities if entity.data['x'] == location_x and entity.data['y'] == location_y]
