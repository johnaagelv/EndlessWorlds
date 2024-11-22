#!/usr/bin/env python3
import traceback, faulthandler
faulthandler.enable()

import tcod

import colours as colour
import exceptions
import input_handlers
import setup_game

def save_game(handler: input_handlers.TBaseEventHandler, filename: str) -> None:
	"""
	If the current handler has an active Engine, save it!
	"""
	if isinstance(handler, input_handlers.TEventHandler):
		handler.engine.save_as(filename)
		print(f"Game '{filename}' saved")

def main() -> None:
	screen_width = 80
	screen_height = 50

	tileset = tcod.tileset.load_tilesheet(
		"dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
	)

	handler: input_handlers.TBaseEventHandler = setup_game.TMainMenu()

	with tcod.context.new_terminal(
		screen_width,
		screen_height,
		tileset=tileset,
		title="Yet Another Roguelike Tutorial",
		vsync=True,
	) as context:
		root_console = tcod.console.Console(screen_width, screen_height, order="F")
		try:
			while True:
				root_console.clear()
				handler.on_render(console=root_console)
				context.present(root_console)
				try:
					for event in tcod.event.wait(timeout=2.0):
						context.convert_event(event)
						handler = handler.handle_events(event)
				except Exception:
					traceback.print_exc()
					if isinstance(handler, input_handlers.TEventHandler):
						handler.engine.message_log.add_message(traceback.format_exc(), colour.error)

		except exceptions.QuitWithoutSaving:
			raise
		except SystemExit: # Save and quit
			if handler.engine:
				save_game(handler, handler.engine.game_name + ".sav")
			raise
		except BaseException: # Save on any other unexpected exception
			save_game(handler, handler.engine.game_name + ".sav")
			raise

if __name__ == "__main__":
	main()
