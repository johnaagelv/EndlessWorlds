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
		self.config = config
		self.tileset = tcod.tileset.load_tilesheet(
			self.config["tileset"], 32, 8, tcod.tileset.CHARMAP_TCOD
		)

		logging.debug(f"- root_console setup")
		self.root_console = tcod.console.Console(
			width = self.config["screen_width"],
			height = self.config["screen_height"],
			order = "F",
		)

		logging.debug(f"- context setup")
		self.context = 	tcod.context.new(
			console = self.root_console,
			tileset = self.tileset,
			title = self.config["title"],
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

		view_width = self.config['viewport_width']
		view_height = self.config['viewport_height']

		self.view_x1 = min(max(0, actor.data['x'] - int(view_width / 2)), width - view_width)
		self.view_x2 = self.view_x1 + view_width

		self.view_y1 = min(max(0, actor.data['y'] - int(view_height / 2)), height - view_height)
		self.view_y2 = self.view_y1 + view_height

		self.root_console.rgb[0:view_width, 0:view_height] = np.select(
			condlist=[visible_tiles[self.view_x1:self.view_x2, self.view_y1:self.view_y2], explored_tiles[self.view_x1:self.view_x2, self.view_y1:self.view_y2]],
			choicelist=[light_tiles[self.view_x1:self.view_x2, self.view_y1:self.view_y2], dark_tiles[self.view_x1:self.view_x2, self.view_y1:self.view_y2]],
			default=tile_types.SHROUD
		)

	"""
	Render the actor on the console from the actor data:
	{x, y, face, colour}
	"""
	def render_actor(self, actor: TActor):
		logging.debug(f"TRender->render_actor( actor )")

		self.root_console.print(
			x = actor.data['x'] - self.view_x1, 
			y = actor.data["y"] - self.view_y1,
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
