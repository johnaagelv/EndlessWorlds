from __future__ import annotations
from pathlib import Path
from logging import DEBUG, INFO, WARNING, FATAL, ERROR  # noqa: F401

""" Client configuration """
GAME_TILESET_FILENAME = Path("client/data/Alloy_curses_12x12.png")
LOG_NAME_CLIENT = "EWclient"
LOG_FILENAME_CLIENT = Path("EWclient.log")
LOG_LEVEL_CLIENT = INFO
CONSOLE_WIDTH = 80
CONSOLE_HEIGHT = 50

""" Server configuration """
LOG_NAME_SERVER = "EWserver"
LOG_FILENAME_SERVER = Path("EWserver.log")
LOG_LEVEL_SERVER = INFO

""" General configuration """
APP_TITLE = "Endless Worlds, 2025 - A multiplayer multiworld roguelike"
APP_AUTHOR = "John Aage Andersen, Latvia"
APP_CONTACT = "j.andersen.lv@gmail.com"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
