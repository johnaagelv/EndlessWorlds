import os
import tcod
from typing import List, Optional

from TActors import TActor
from TActions import TAction, TGameQuitAction, TGameNewAction, TGameLoadAction

class TStartupMenuHandler(tcod.event.EventDispatch[TAction]):
	def __init__(self, choices: List) -> None:
		super().__init__()
		self.choices = choices

	def ev_quit(self, event: tcod.event.Quit) -> TAction:
		return TGameQuitAction()
	
	def ev_keydown(self, event: "tcod.event.KeyDown") -> Optional[TAction]:
		action : Optional[TAction] = None
		key = event.sym
		print(key)
#		print(f"key={key}, {chr(key)}")		
		if chr(key) in self.choices.keys():
			if self.choices[chr(key)]["action"] == "GameNew":
				action = TGameNewAction()
			elif self.choices[chr(key)]["action"] == "GameLoad":
				action = TGameLoadAction(self.choices[chr(key)])
			elif self.choices[chr(key)]["action"] == "GameQuit":
				action = TGameQuitAction()

		return action
	

"""
TPlayStartup initializes the player to a new game or the current game
- Initialize user interface
- Present and get user choice
- Initialize player by user choice
"""
class TPlayStartup():
	def __init__(self):
		# Initialize user interface
		self.screen_width = 80
		self.screen_height = 44
		# Get the games available - new game and saved game
		save_games = os.listdir("save/")
		save_games.sort()

		self.choices = {
			"a": {"title":"New game", "action":"GameNew", "file":"new/new_game.sav"},
		}

		for i, filename in enumerate(
			save_games
		):
			game_title = filename.replace('.sav','')
			self.choices[chr(66+i).lower()] = {"title":game_title, "action":"GameLoad", "file":"save/"+filename}

		self.choices["q"] = {"title":"Quit", "action":"GameQuit", "file":""}
		self.choices[chr(27)] = {"title":"", "action":"GameQuit", "file":""}

		# Load a background image
		self.background_image = tcod.image.load("images/startup.png")[:, :, :3]
		# Load the tileset
		self.tileset = tcod.tileset.load_tilesheet(
			"dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
		)

	def run(self, actor: TActor) -> bool:
		print("TPlayStartup.run(actor)")
		# Attach the event handler for the startup menu
		menu_handler = TStartupMenuHandler(self.choices)

		with tcod.context.new(
			columns=self.screen_width,
			rows=self.screen_height,
			tileset=self.tileset,
			title="Endless Worlds",
			vsync=True
		) as context:

			console = tcod.Console(self.screen_width, self.screen_height, order="F")

			"""Render the main menu on a background image."""
			console.draw_semigraphics(self.background_image, 0, 0)

			console.print(
				x=2,
				y=2,
				string="ENDLESS WORLDS",
				fg=(255, 255, 255), #colour.menu_title,
				alignment=tcod.LEFT,
			)
			console.print(
				x=2,
				y=console.height - 2,
				string="By John Aage Andersen",
				fg=(255, 255, 255), #color.menu_title,
				alignment=tcod.LEFT,
			)

			menu_width = 40
			i = 6
			for choice_key in self.choices.keys():
				if not self.choices[choice_key]["title"] == "":
					menu_choice = "["+choice_key+"] "+self.choices[choice_key]["title"]
					console.print(
						x=2,
						y=i,
						string=menu_choice.ljust(menu_width),
						fg=(255,255,255), #color.menu_text,
	#					bg=(0,0,0), #color.black,
						alignment=tcod.LEFT,
						bg_blend=tcod.BKGND_ALPHA(64),
					)
					i += 2

			context.present(console)

			is_running = True
			time_counter = 0.0
			while is_running == True:
				for event in tcod.event.wait():
					action = menu_handler.dispatch(event)
					if action is None:
						continue

					action.run(actor)
					if not actor.is_playing:
						is_running = False
						continue

"""
TPlayShutdown saves the current game
"""
class TPlayShutdown():
	def __init__(self):
		pass

	def run(self, player: TActor) -> None:
		pass