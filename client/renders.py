from typing import Reversible
import logging

import textwrap
import tcod
import numpy as np
import tile_types
from entities import TActor
from message_logs import TLogMessage
import client.ui.colours as colours
logger = logging.getLogger("EWClient")

class TRender:
	def __init__(self, config):
#		logging.info(f"TRender->__init__( config )")
#		logging.info(f"- tileset setup")
		self.config = config
		self.tileset = tcod.tileset.load_tilesheet(
			self.config["tileset"], 16, 16, tcod.tileset.CHARMAP_CP437
		)

#		logging.info(f"- root_console setup")
		self.root_console = tcod.console.Console(
			width = self.config["screen_width"],
			height = self.config["screen_height"],
			order = "F",
		)

#		logging.info(f"- context setup")
		self.context = 	tcod.context.new(
			console = self.root_console,
			tileset = self.tileset,
			title = "Endless Worlds, (c) 2025",
			vsync = True,
		)

	"""
	Render the map on the console from the map data
	{width, height, tiles}
	"""
	def render_world(self, actor: TActor):
#		logging.debug(f"TRender->render_world( actor )")
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
#		logging.debug(f"TRender->render_actor( actor )")

		self.root_console.print(
			x = actor.data['x'] - self.view_x1, 
			y = actor.data["y"] - self.view_y1,
			text = actor.data["face"],
			fg=actor.data["colour"],
		)

		if actor.map['name']:
			self.root_console.print(
				x = 61,
				y = 1,
				text = actor.map['name'],
				fg=actor.data["colour"]
			)
	
	def render_entities(self, actor: TActor):
#		logging.debug(f"TRender->render_entities( actor )")
		map = actor.map
		visible_tiles = map['visible']
		for entity in actor.data['world'].entities:
			if visible_tiles[entity['x'], entity['y']]:
				self.root_console.print(x=entity['x'], y=entity['y'], text=entity['face'], fg=entity['colour'])

	def render_states(self, actor: TActor):
#		logging.debug(f"TRender->render_states( states )")
		view_x = self.config['state_x']
		view_y = self.config['state_y']
		view_width = self.config['state_width']
		#view_height = self.config['state_height']
		state_keys = actor.data['states'].keys()
		for state_key in state_keys:
			state = actor.data['states'][state_key]
			current_value = int(state[0] / 1000)
			max_value = int(state[2] / 1000)
			bar_width = int(float(state[0]) / state[2] * view_width)
			bar_level = float(current_value / max_value)
			bar_filled = colours.bar_low
			if bar_level > 0.3:
				bar_filled = colours.bar_high
			elif bar_level > 0.2:
				bar_filled = colours.bar_medium

			self.root_console.draw_rect(x=view_x, y=view_y, width=view_width, height=1, ch=1, bg=colours.bar_empty)
			if bar_width > 0:
				self.root_console.draw_rect(x=view_x, y=view_y, width=bar_width, height=1, ch=1, bg=bar_filled)
			self.root_console.print(x=view_x + 1, y=view_y, text=f"{state_key}", fg=colours.bar_text)
			state_x = view_width - 2 - (current_value > 9) - (current_value > 99) - (current_value > 999)
			self.root_console.print(x=view_x + state_x, y=view_y, text=f"{current_value}", fg=colours.bar_text)
			view_y += 1

	"""
	Render messages
	"""
	def render_log(self, messages) -> None:
		x = self.config['log_x']
		y = self.config['log_y']
		width = self.config['log_width']
		height = self.config['log_height']
		self.render_messages(
			self.root_console,
			x, y, width, height,
			messages
		)

	@staticmethod
	def render_messages(
		console: tcod.console.Console,
		x: int,
		y: int,
		width: int,
		height: int,
		messages: Reversible[TLogMessage]
	) -> None:
		y_offset = height - 1
		for message in reversed(messages):
			for line in reversed(textwrap.wrap(message.full_text, width)):
				console.print(x=x, y=y + y_offset, text=line, fg=message.fg)
				y_offset -= 1
				if y_offset < 0:
					return
	
	"""
	Render the console
	"""
	def render(self):
#		logging.info(f"TRender->render()")
		# Present the console
		self.context.present(self.root_console)
		# Clear the console for a new presentation
		self.root_console.clear()
