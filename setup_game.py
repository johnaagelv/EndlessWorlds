from __future__ import annotations
import os
import copy
import lzma
import pickle
import traceback
import exceptions
from typing import Optional

import tcod
import tcod.libtcodpy as tcodformat

import colours as colour
from engine import TEngine
import entity_factories
from game_map import TWorld
import input_handlers

background_image = tcod.image.load("menu_background.png")[:, :, :3]

def new_game() -> TEngine:
	map_width = 80
	map_height = 43

	player = copy.deepcopy(entity_factories.player)
	engine = TEngine(player=player)

	engine.game_name = "Endless Worlds, Planet Ankt"

	engine.game_world = TWorld(
		engine=engine,
		map_width=map_width,
		map_height=map_height,
	)
	engine.game_world.generate_floor()
	engine.update_fov()

	engine.message_log.add_message(
		"Hello and welcome, Adventurer, to Endless Worlds!", colour.welcome_text
	)
	return engine

def load_game(filename: str) -> TEngine:
	"""
	Load an engine instance from a file
	"""
	with open(filename, "rb") as f:
		engine = pickle.loads(lzma.decompress(f.read()))
		assert isinstance(engine, TEngine)
		return engine

def get_saved_games() -> list:
	return [x for x in os.listdir(".") if x.endswith(".sav")]

class TMainMenu(input_handlers.TBaseEventHandler):
	"""
	Handle the main menu rendering and input
	"""
	def __init__(self) -> None:
		self.menu_choices = dict()
		self.menu_choices["0"] = "Quit"
		self.menu_choices["1"] = "New game"
		for i, saved_game in enumerate(get_saved_games()):
			game_name, game_ext = saved_game.split(".")
			self.menu_choices[chr(ord("a") + i)] = game_name

	def on_render(self, console: tcod.console.Console) -> None:
		"""
		Render the main menu on a background image
		"""
		console.draw_semigraphics(background_image, 0, 0)
		for i, text in enumerate(
			["### ENDLESS WORLDS ###", " ", "Planet Ankt"]
		):
			console.print(
				console.width // 2,
				console.height // 2 - 8 + i, 
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
		i = 0
		for menu_key in self.menu_choices:
			console.print(
				console.width // 2,
				console.height // 2 - 2 + i,
				(menu_key + ". " + self.menu_choices[menu_key]).ljust(menu_width),
				fg=colour.menu_text,
				bg=colour.black,
				alignment=tcodformat.CENTER,
				bg_blend=tcodformat.BKGND_ALPHA(64),
			)
			i += 1
	
	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[input_handlers.TBaseEventHandler]:
		if event.sym in (tcod.event.KeySym.N0, tcod.event.KeySym.KP_0, tcod.event.KeySym.ESCAPE):
			raise exceptions.QuitWithoutSaving()
		
		elif tcod.event.KeySym.a <= event.sym <= tcod.event.KeySym.z:
			try:
				return input_handlers.TMainGameEventHandler(load_game(self.menu_choices[chr(event.sym)] + ".sav"))
			except FileNotFoundError:
				return input_handlers.TPopupMessage(self, "No saved game to load!")
			except Exception as exc:
				traceback.print_exc()
				return input_handlers.TPopupMessage(self, f"Failed to load save:\n{exc}")

		elif event.sym in (tcod.event.KeySym.N1, tcod.event.KeySym.KP_1):
			return input_handlers.TMainGameEventHandler(new_game())
		
		return None