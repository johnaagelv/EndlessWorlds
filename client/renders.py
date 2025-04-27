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

		self.root_console.rgb[0:width, 0:height] = np.select(
			condlist=[visible_tiles, explored_tiles],
			choicelist=[light_tiles, dark_tiles],
			default=tile_types.SHROUD
		)

	"""
	Render the actor on the console from the actor data:
	{x, y, face, colour}
	"""
	def render_actor(self, actor: TActor):
		logging.debug(f"TRender->render_actor( actor )")
		self.root_console.print(
			x = actor.data["x"], 
			y = actor.data["y"],
			string = actor.data["face"],
			fg=actor.data["colour"],
		)
	
	"""
	Render the console
	"""
	def render(self):
		logging.debug(f"TRender->render()")
		# Present the console
		self.context.present(self.root_console)
		# Clear the console for a new presentation
		self.root_console.clear()
