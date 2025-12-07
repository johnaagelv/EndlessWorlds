from __future__ import annotations
from pathlib import Path
from logging import DEBUG, INFO, WARNING, FATAL, ERROR  # noqa: F401

""" Community configuration """
GAME_TILESET_FILENAME = Path("community/ui/redjack17.png") #Path("client/data/Alloy_curses_12x12.png")
LOG_NAME = "EWcommunity"
LOG_FILENAME = Path("EWcommunity.log")
LOG_LEVEL = INFO
GAME_HOST = "192.168.1.104"
GAME_PORT = 25261

""" Player configuration """
"""
Actor states, where:
- name, used for presenting
- value, current value of the state
- max, maximum value of the state
- usage, use of the state per tick
"""
ACTOR_STATES = [
	["Health", 500000, 1000000, -1],
	["Strength", 500000, 1000000, -1],
	["Energy", 500000, 1000000, -1]
]

""" General configuration """
APP_TITLE = "Endless Worlds, 2025 - A multiplayer multiworld roguelike"
APP_AUTHOR = "John Aage Andersen, Latvia"
APP_CONTACT = "j.andersen.lv@gmail.com"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
