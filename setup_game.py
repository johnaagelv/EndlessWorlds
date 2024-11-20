from __future__ import annotations

import copy
from typing import Optional

import tcod
import tcod.libtcodpy as tcodformat

import colours as colour
from engine import TEngine
import entity_factories
import input_handlers
from procgen import generate_dungeon

background_image = tcod.image.load("menu_background.png")[:, :, :3]

def new_game() -> TEngine:
	map_width = 80
	map_height = 43

	player = copy.deepcopy(entity_factories.player)
	engine = TEngine(player=player)

	engine.game_map = generate_dungeon(
		map_width=map_width,
		map_height=map_height,
		engine=engine,
	)
	engine.update_fov()

	engine.message_log.add_message(
		"Hello and welcome, Adventurer, to Endless Worlds!", colour.welcome_text
	)
	return engine

class TMainMenu(input_handlers.TBaseEventHandler):
	"""
	Handle the main menu rendering and input
	"""
	def on_render(self, console: tcod.console.Console) -> None:
		"""
		Render the main menu on a background image
		"""
		console.draw_semigraphics(background_image, 0, 0)
		for i, text in enumerate(
			["ENDLESS WORLDS", "Planet Ankt, Camp Landing"]
		):
			console.print(
				console.width // 2,
				console.height // 2 - 5 + i, 
				text,
				fg=colour.menu_title,
				alignment=tcodformat.CENTER,
			)

		console.print(
			console.width // 2,
			console.height - 2,
			"By John Aage Andersen",
			fg=colour.menu_title,
			alignment=tcodformat.CENTER,
		)

		menu_width = 35
		for i, text in enumerate(
			["[N] New game", "[C] Continue last game", "[Q] Quit"]
		):
			console.print(
				console.width // 2,
				console.height // 2 - 2 + i,
				text.ljust(menu_width),
				fg=colour.menu_text,
				bg=colour.black,
				alignment=tcodformat.CENTER,
				bg_blend=tcodformat.BKGND_ALPHA(64),
			)
	
	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[input_handlers.TBaseEventHandler]:
		if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
			raise SystemExit()
		
		elif event.sym == tcod.event.KeySym.c:
			# TODO: Load the game here
			pass

		elif event.sym == tcod.event.KeySym.n:
			return input_handlers.TMainGameEventHandler(new_game())
		
		return None