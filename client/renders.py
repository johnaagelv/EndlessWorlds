import tcod
import numpy as np
import tile_types
from entities import TActor

class TRender:
	def __init__(self, config):
		self.tileset = tcod.tileset.load_tilesheet(
			config["tileset"], 32, 8, tcod.tileset.CHARMAP_CP437
		)

		self.root_console = tcod.console.Console(
			config["screen_width"],
			config["screen_height"],
			order="F",
		)
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
		map = actor.map
		visible_tiles = map['visible']
		explored_tiles = map['explored']
		light_tiles = map['tiles']['light']
		dark_tiles = map['tiles']['dark']

		width = map["width"]
		height = map["height"]
#		self.root_console.rgb[0:width, 0:height] = map["tiles"]["dark"]
		self.root_console.rgb[0:width, 0:height] = np.select(
			condlist=[visible_tiles, explored_tiles],
			choicelist=[light_tiles, dark_tiles],
			default=tile_types.SHROUD
		)

	"""
	Render the actor on the console from the actor data:
	{x, y, face, colour}
	"""
	def render_actor(self, actor):
		self.root_console.print(
			x = actor["x"], 
			y = actor["y"],
			string = actor["face"],
			fg=actor["colour"],
		)
	
	"""
	Render the console
	"""
	def render(self):
		# Present the console
		self.context.present(self.root_console)
		# Clear the console for a new presentation
		self.root_console.clear()
