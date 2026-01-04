from __future__ import annotations

import attrs
import numpy as np
import tcod.console
import tcod.event
from tcod.event import KeySym, Modifier

import client.g as g
from client.constants import DIRECTION_KEYS, ACTION_KEYS, STAIR_KEYS
from client.game.state import Pop, Push, Reset, State, StateResult
from client.game.components import CID, Maps, Position, Vision, World
from client.game.tags import IsPlayer, IsWorld
import client.tile_types as tile_types
import client.game.world_tools as world_tools
import client.game.entity_tools as entity_tools
import client.game.menus
import client.game.connect_tools
import client.game.render_tools as renders
import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

@attrs.define()
class InGame(State):
	""" Primary in-game state """

	def on_event(self, event: tcod.event.Event) -> StateResult:
		""" Handle events for the in-game state """
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
		(world,) = g.game.Q.all_of(tags=[IsWorld])
		pos = player.components[Position]
		match event:
		
			case tcod.event.KeyDown(sym=sym, mod=mod) if (sym, mod) in STAIR_KEYS:
				action = STAIR_KEYS[sym, mod]
				if world_tools.in_gateway(player.components[Position].x, player.components[Position].y, player.components[Position].m):
					gateway = world_tools.go_gateway(player.components[Position].x, player.components[Position].y, player.components[Position].m, action)
					world_tools.start_map(gateway["gateway"]["m"])
					# Move to x, y coordinate in map number m
					player.components[Position] = Position(gateway["gateway"]["x"], gateway["gateway"]["y"], gateway["gateway"]["m"])

			case tcod.event.KeyDown(sym=sym, mod=mod) if (sym, mod) in ACTION_KEYS:
				match (sym, mod):
					case (KeySym.D, Modifier.NONE):
						return Push(Drop())
					case (KeySym.COMMA, Modifier.NONE):
						if world_tools.pickable_items_near(pos):
							return Push(PickupMenu())
				return None

			case tcod.event.KeyDown(sym=sym) if sym in DIRECTION_KEYS:
				player.components[Position] += DIRECTION_KEYS[sym]
				new_pos = player.components[Position]
				map = world.components[Maps].maps[new_pos.m]
				vision_radius = player.components[Vision]
				if map["overworld"] and not (vision_radius - 1 < new_pos.x < map["width"] - vision_radius and vision_radius - 1 < new_pos.y < map["height"] - vision_radius):
					ww = map["ww"]
					wh = map["wh"]
					new_x = new_pos.x
					new_y = new_pos.y
					if new_x < 0:
						new_x = map["width"] - 1
						ww = (ww - 1) % world.components[World].width
					if new_x >= map["width"]:
						new_x = 0
						ww = (ww + 1) % world.components[World].width
					if new_y < 0:
						new_y = map["height"] - 1
						wh = (wh - 1) % world.components[World].height
					if new_y >= map["height"]:
						new_y = 0
						wh = (wh + 1) % world.components[World].height
					m = ww * world.components[World].width + wh
					logging.debug(f"Switch to map {m} based on {ww} and {wh}")
					world_tools.start_map(m)
					player.components[Position] = Position(new_x, new_y, m)
					return None
				
				if world_tools.in_gateway(new_pos.x, new_pos.y, new_pos.m):
					gateway = world_tools.go_gateway(new_pos.x, new_pos.y, new_pos.m)
					world_tools.start_map(gateway["gateway"]["m"])
					# Move to x, y coordinate in map number m
					player.components[Position] = Position(gateway["gateway"]["x"], gateway["gateway"]["y"], gateway["gateway"]["m"])
				return None

			case tcod.event.KeyDown(sym=KeySym.ESCAPE):
				return Push(MainMenu())

			case tcod.event.Quit():
				return Push(MainMenu())

			case _:
				return None

	def on_draw(self, console: tcod.console.Console) -> None:
		""" Draw the stancard screen """
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
		pos = player.components[Position]
		vision = player.components[Vision]
		(world,) = g.game.Q.all_of(tags=[IsWorld])
		maps = world.components[Maps].maps
		world_width = world.components[World].width
		world_height = world.components[World].height
		render_map: dict = {}
		if not maps[pos.m]["overworld"]:
			render_map = maps[pos.m]
		else:
			ww = world.components[Maps].maps[pos.m]["ww"]
			wh = world.components[Maps].maps[pos.m]["wh"]
			map_width = world.components[Maps].maps[pos.m]["width"]
			map_height = world.components[Maps].maps[pos.m]["height"]
#			print(f"{map_width},{map_height}")

			qul = ((ww - 1) % world_width) * world_width + (wh - 1) % world_height # Quadrant upper left
			qml = ((ww - 1) % world_width) * world_width + (wh - 0) % world_height # Quadrant left
			qll = ((ww - 1) % world_width) * world_width + (wh + 1) % world_height # Quadrant lower left
			qum = ((ww - 0) % world_width) * world_width + (wh - 1) % world_height
			qmm = ((ww - 0) % world_width) * world_width + (wh - 0) % world_height
			qlm = ((ww - 0) % world_width) * world_width + (wh + 1) % world_height
			qur = ((ww + 1) % world_width) * world_width + (wh - 1) % world_height
			qmr = ((ww + 1) % world_width) * world_width + (wh - 0) % world_height
			qlr = ((ww + 1) % world_width) * world_width + (wh + 1) % world_height
#			print(f"{qul},{qml},{qll} {qum},{qmm},{qlm} {qur},{qmr},{qlr}")
			world_tools.start_map(qul)
			world_tools.start_map(qml)
			world_tools.start_map(qll)
			world_tools.start_map(qum)
			world_tools.start_map(qmm)
			world_tools.start_map(qlm)
			world_tools.start_map(qur)
			world_tools.start_map(qmr)
			world_tools.start_map(qlr)
			logger.debug(f"*** qul light tiles {qul} ***")
			logger.debug(world.components[Maps].maps[0]["tiles"]['light'])

			maps_left: dict = {}
			maps_left["visible"] = np.concatenate((maps[qul]["visible"], maps[qml]["visible"], maps[qll]["visible"]), axis=1)
			maps_left["explored"] = np.concatenate((maps[qul]["explored"], maps[qml]["explored"], maps[qll]["explored"]), axis=1)
			maps_left["tiles"] = np.concatenate((maps[qul]["tiles"], maps[qml]["tiles"], maps[qll]["tiles"]), axis=1, dtype=tile_types.tile_dt)
			maps_left["dark"] = np.concatenate((maps[qul]["tiles"]["dark"], maps[qml]["tiles"]["dark"], maps[qll]["tiles"]["dark"]), axis=1, dtype=tile_types.graphic_dt)
			maps_left["light"] = np.concatenate((maps[qul]["tiles"]["light"], maps[qml]["tiles"]["light"], maps[qll]["tiles"]["light"]), axis=1, dtype=tile_types.graphic_dt)
			maps_left["transparent"] = np.concatenate((maps[qul]["tiles"]["transparent"], maps[qml]["tiles"]["transparent"], maps[qll]["tiles"]["transparent"]), axis=1)
#			logger.debug(maps_left['light'])
#			raise SystemExit

			maps_middle: dict = {}
			maps_middle["visible"] = np.concatenate((maps[qum]["visible"], maps[qmm]["visible"], maps[qlm]["visible"]), axis=1)
			maps_middle["explored"] = np.concatenate((maps[qum]["explored"], maps[qmm]["explored"], maps[qlm]["explored"]), axis=1)
			maps_middle["tiles"] = np.concatenate((maps[qum]["tiles"], maps[qmm]["tiles"], maps[qlm]["tiles"]), axis=1, dtype=tile_types.tile_dt)
			maps_middle["dark"] = np.concatenate((maps[qum]["tiles"]["dark"], maps[qmm]["tiles"]["dark"], maps[qlm]["tiles"]["dark"]), axis=1, dtype=tile_types.graphic_dt)
			maps_middle["light"] = np.concatenate((maps[qum]["tiles"]["light"], maps[qmm]["tiles"]["light"], maps[qlm]["tiles"]["light"]), axis=1, dtype=tile_types.graphic_dt)
			maps_middle["transparent"] = np.concatenate((maps[qum]["tiles"]["transparent"], maps[qmm]["tiles"]["transparent"], maps[qlm]["tiles"]["transparent"]), axis=1)

			maps_right: dict = {}
			maps_right["visible"] = np.concatenate((maps[qur]["visible"], maps[qmr]["visible"], maps[qlr]["visible"]), axis=1)
			maps_right["explored"] = np.concatenate((maps[qur]["explored"], maps[qmr]["explored"], maps[qlr]["explored"]), axis=1)
			maps_right["tiles"] = np.concatenate((maps[qur]["tiles"], maps[qmr]["tiles"], maps[qlr]["tiles"]), axis=1, dtype=tile_types.tile_dt)
			maps_right["dark"] = np.concatenate((maps[qur]["tiles"]["dark"], maps[qmr]["tiles"]["dark"], maps[qlr]["tiles"]["dark"]), axis=1, dtype=tile_types.graphic_dt)
			maps_right["light"] = np.concatenate((maps[qur]["tiles"]["light"], maps[qmr]["tiles"]["light"], maps[qlr]["tiles"]["light"]), axis=1, dtype=tile_types.graphic_dt)
			maps_right["transparent"] = np.concatenate((maps[qur]["tiles"]["transparent"], maps[qmr]["tiles"]["transparent"], maps[qlr]["tiles"]["transparent"]), axis=1)

			render_map["visible"] = np.concatenate((maps_left["visible"], maps_middle["visible"], maps_right["visible"]), axis=0)
			render_map["explored"] = np.concatenate((maps_left["explored"], maps_middle["explored"], maps_right["explored"]), axis=0)
			render_map["tiles"] = np.concatenate((maps_left["tiles"], maps_middle["tiles"], maps_right["tiles"]), axis=0, dtype=tile_types.tile_dt)
			render_map["dark"] = np.concatenate((maps_left["dark"], maps_middle["dark"], maps_right["dark"]), axis=0, dtype=tile_types.graphic_dt)
			render_map["light"] = np.concatenate((maps_left["light"], maps_middle["light"], maps_right["light"]), axis=0, dtype=tile_types.graphic_dt)
			render_map["transparent"] = np.concatenate((maps_left["transparent"], maps_middle["transparent"], maps_right["transparent"]), axis=0)
			
			render_map["width"] = map_width * 3
			render_map["height"] = map_height * 3
			render_map["name"] = world.components[Maps].maps[pos.m]["name"]
			render_map["items"] = world.components[Maps].maps[pos.m]["items"]

			pos = Position(pos.x + map_width, pos.y + map_height, pos.m)

		render_map = entity_tools.fov(pos, vision, render_map)

		# Get the view port for the rendering methods
		view_port = world_tools.get_view_port(pos, render_map)

		if maps[pos.m]["overworld"]:
#			logger.debug(" explored ")
#			logger.debug(world.components[Maps].maps[qul]["explored"][map_width - 10:map_width,map_height - 10:map_height])
#			logger.debug(render_map["explored"][map_width - 10:map_width, map_height - 10:map_height])
#			logger.debug(" visible ")
#			logger.debug(world.components[Maps].maps[qul]["visible"][map_width - 10:map_width,map_height - 10:map_height])
#			logger.debug(render_map['visible'][map_width - 10:map_width, map_height - 10:map_height])
#			logger.debug(render_map['dark'][map_width - 10:map_width, map_height - 10:map_height])
#			logger.debug(render_map['light'][map_width - 10:map_width, map_height - 10:map_height])
			# transfer the visible back into visible and explored in quadrants 
			world.components[Maps].maps[qul]["visible"] = render_map["visible"][0:map_width, 0:map_height]
			world.components[Maps].maps[qul]["explored"] |= world.components[Maps].maps[qul]["visible"]
			world.components[Maps].maps[qml]["visible"] = render_map["visible"][0:map_width, map_height:map_height * 2]
			world.components[Maps].maps[qml]["explored"] |= world.components[Maps].maps[qml]["visible"]
			world.components[Maps].maps[qll]["visible"] = render_map["visible"][0:map_width, map_height * 2:map_height * 3]
			world.components[Maps].maps[qll]["explored"] |= world.components[Maps].maps[qll]["visible"]
			world.components[Maps].maps[qum]["visible"] = render_map["visible"][map_width:map_width * 2, 0:map_height]
			world.components[Maps].maps[qum]["explored"] |= world.components[Maps].maps[qum]["visible"]
			world.components[Maps].maps[qmm]["visible"] = render_map["visible"][map_width:map_width * 2, map_height:map_height * 2]
			world.components[Maps].maps[qmm]["explored"] |= world.components[Maps].maps[qmm]["visible"]
			world.components[Maps].maps[qlm]["visible"] = render_map["visible"][map_width:map_width * 2, map_height * 2:map_height * 3]
			world.components[Maps].maps[qlm]["explored"] |= world.components[Maps].maps[qlm]["visible"]

		# Render the current map
		renders.world_map(current_map=render_map, console=console, view_port=view_port)

		# Draw the entities including the player
#		renders.entities(pos.m, console, view_port)
		renders.player(player, console, view_port, pos)

		# Draw the player information
		renders.player_states(player, console)
		
		# Draw any messages
		if text := g.game[None].components.get(("Text", str)):
			console.print(x=0, y=console.height - 1, text=text, fg=(255, 255, 255), bg=(0, 0, 0))

	def on_connect(self) -> None:
		""" Connect to the server for information"""
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
		pos = player.components[Position]
		cid = player.components[CID]
		(world,) = g.game.Q.all_of(tags=[IsWorld])
		maps = world.components[Maps]

		fos_request = {
			"cmd": "fos",
			"cid": cid,
			"x": pos.x,
			"y": pos.y,
			"m": pos.m,
			"r": player.components[Vision],
		}
		result = client.game.connect_tools.query_server(fos_request)
		x_min = result["x_min"]
		x_max = result["x_max"]
		y_min = result["y_min"]
		y_max = result["y_max"]

		temp = np.array(result['view'])
		maps.maps[pos.m]["tiles"][x_min:x_max, y_min:y_max] = temp
		maps.maps[pos.m]["actors"] = result["actors"]
		
		item_temp = np.array(result['items'])
		maps.maps[pos.m]["items"] = item_temp
		
		world.components[Maps] = Maps(maps.maps, maps.defs)
		return None

class MainMenu(client.game.menus.ListMenu):
	""" Main/escape menu """
	__slots__ = ()

	def __init__(self) -> None:
		""" Initialize the main menu """
		items = [
			client.game.menus.SelectItem("New game", self.new_game, {id:100}),
		]
		if hasattr(g, "world"):
			# We got a world, so add the continue menu item
			items.append(client.game.menus.SelectItem("Continue", self.continue_, {id:800}))

		# Add the quit menu item
		items.append(client.game.menus.SelectItem("Quit", self.quit, {id:900}))

		super().__init__(
			items=tuple(items),
			selected=0,
			x=5,
			y=5,
		)

	@staticmethod
	def continue_(item: dict) -> StateResult:
		""" Return to the game """
		return Reset(InGame())
	
	@staticmethod
	def new_game(item: dict) -> StateResult:
		""" Begin a new game """
		g.game = world_tools.new_game()
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
		world_tools.start_map( player.components[Position].m )
		return Reset(InGame())

	@staticmethod
	def quit(item: dict) -> StateResult:
		""" Close the program """
		raise SystemExit

class PickupMenu(client.game.menus.ListMenu):
	""" Pickup menu """
	__slots__ = ()

	def __init__(self) -> None:
		""" Initialize the pickup menu """
		items = [
		]
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
		pos = player.components[Position]
		map_items = world_tools.get_items_by_location(pos=pos)
		unique_items: dict = {}
		for item in map_items:
			if item["name"] in unique_items.keys():
				unique_items[item["name"]]["count"] += 1
			else:
				unique_items[item["name"]] = {
					"count": 1,
					"face": item["face"], 
					"name": item["name"],
					"iid": item["iid"]
				}

		item_idx = 0		
		for item in unique_items.keys():
			items.append(client.game.menus.SelectItem(f"{unique_items[item]["count"]:4d} {item}", self.pickup, unique_items[item]))
			item_idx += 1

		super().__init__(
			items=tuple(items),
			selected=0,
			x=5,
			y=5,
		)
	
	def pickup(self, item: dict) -> StateResult:
		""" Return to the game """
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
		pos = player.components[Position]
		request = {
			"cmd": "get",
			"m": pos.m,
			"iid": item["iid"]
		}
		result = client.game.connect_tools.query_server(request)
		if result["iid"] == request["iid"]:
			print(f"Got {item}")
		return Reset(InGame())

@attrs.define()
class Pickup(State):
	def on_event(self, event: tcod.event.Event) -> StateResult:
		""" Handle events for picking up items from player location """
		match event:
			case tcod.event.KeyDown(sym=KeySym.ESCAPE):
				return Pop()
		return None
	
	def on_draw(self, console: tcod.console.Console) -> None:
		""" Present the items on player location available for pickup """
		(player,) = g.game.Q.all_of(tags=[IsPlayer])
		pos = player.components[Position]
		(world,) = g.game.Q.all_of(tags=[IsWorld])
		visible_tiles = world.components[Maps].maps[pos.m]["visible"]
		map_items = world.components[Maps].maps[pos.m]["items"]
		unique_items: dict = {}
		for item in [item for item in map_items if pos.x - 1 <= item["x"] <= pos.x + 1 and pos.y - 1 <= item["y"] <= pos.y + 1 and visible_tiles[item["x"], item["y"]]]:
			
			if item["name"] in unique_items.keys():
				unique_items[item["name"]] += 1
			else:
				unique_items[item["name"]] = 1
		
		y: int = 10
		for item in unique_items.keys():
			console.print(40, y, text=f"{unique_items[item]} {item}")
			y+=1

		return None

@attrs.define()
class Drop(State):
	def on_event(self, event: tcod.event.Event) -> StateResult:
		""" Handle events for dropping items from the inventory """
		return Pop()
	
	def on_draw(self, console: tcod.console.Console) -> None:
		""" Present the inventory for item drop """
		return None
