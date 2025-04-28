import logging
logger = logging.getLogger("EWClient")

import tcod
import numpy as np
import tile_types
from entities import TActor

class TRender:
	def __init__(self, config):
		logging.debug(f"TRender->__init__( config )")
		logging.debug(f"- tileset setup")
		self.tileset = tcod.tileset.load_tilesheet(
			config["tileset"], 32, 8, tcod.tileset.CHARMAP_TCOD
		)

		logging.debug(f"- root_console setup")
		self.root_console = tcod.console.Console(
			width = config["screen_width"],
			height = config["screen_height"],
			order = "F",
		)

		logging.debug(f"- context setup")
		self.context = 	tcod.context.new(
			console = self.root_console,
			tileset = self.tileset,
			title = config["title"],
			vsync = True,
		)

	"""
	Render the map on the console from the map data
	{width, height, tiles}
	"""
	def render_world(self, actor: TActor):
		logging.debug(f"TRender->render_world( actor )")
		actor.update_fos()
		map = actor.map
		visible_tiles = map['visible']
		explored_tiles = map['explored']
		light_tiles = map['tiles']['light']
		dark_tiles = map['tiles']['dark']

		width = map["width"]
		height = map["height"]

		view_width = self.root_console.width
		view_height = self.root_console.height - 5

		print(f"actor ({actor.data['x']},{actor.data['y']})")
		print(f"- viewport ({view_width},{view_height}) - map ({width},{height})")
		view_x1 = min(max(0, actor.data['x'] - int(view_width / 2)), width - view_width)
		view_x2 = view_x1 + view_width
		print(f"- x1:x2: {view_x1}:{view_x2}")

		view_y1 = max(0, actor.data['y'] - int(height / 2))
		view_y2 = min(height, actor.data['y'] + int(height / 2))

		self.root_console.rgb[0:width, 0:height] = np.select(
			condlist=[visible_tiles[view_x1:view_x2], explored_tiles[view_x1:view_x2]],
			choicelist=[light_tiles[view_x1:view_x2], dark_tiles[view_x1:view_x2]],
			default=tile_types.SHROUD
		)

	"""
	Render the actor on the console from the actor data:
	{x, y, face, colour}
	"""
	def render_actor(self, actor: TActor):
		logging.debug(f"TRender->render_actor( actor )")

		map = actor.map
		width = map["width"]
		height = map["height"]

		view_width = self.root_console.width
		view_height = self.root_console.height - 5
		view_x1 = min(max(0, actor.data['x'] - int(view_width / 2)), width - view_width)
		view_x2 = view_x1 + view_width

		self.root_console.print(
			x = actor.data['x'] - view_x1, 
			y = actor.data["y"],
			string = actor.data["face"],
			fg=actor.data["colour"],
		)
	
	"""
	Render the console
	"""
	def render(self):
		logging.info(f"TRender->render()")
		# Present the console
		self.context.present(self.root_console)
		# Clear the console for a new presentation
		self.root_console.clear()
