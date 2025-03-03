import tcod


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
	def render_world(self, map):
		width = map["width"]
		height = map["height"]
		self.root_console.rgb[0:width, 0:height] = map["tiles"]["dark"]

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
