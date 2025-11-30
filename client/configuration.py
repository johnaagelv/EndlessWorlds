from __future__ import annotations
from pathlib import Path
from logging import DEBUG, INFO, WARNING, FATAL, ERROR  # noqa: F401

""" Client configuration """
GAME_TILESET_FILENAME = Path("client/data/redjack17.png") #Path("client/data/Alloy_curses_12x12.png")
LOG_NAME_CLIENT = "EWclient"
LOG_FILENAME_CLIENT = Path("EWclient.log")
LOG_LEVEL_CLIENT = INFO
CONSOLE_WIDTH = 80
CONSOLE_HEIGHT = 50
GAME_HOST = "192.168.1.104"
GAME_PORT = 25261

""" Player configuration """

"""
Player states, where:
- name, used for presenting
- value, current value of the state
- max, maximum value of the state
- usage, use of the state per tick
"""
PLAYER_STATES = [
	["Health", 500000, 1000000, -1],
	["Energy", 500000, 1000000, -1]
]

"""
UI layout - 1: Map view port; 2: Message view port; 3: World and player states view port
+------------+--+
|            |  |
|     1      |  |
|            | 3|
+------------+  |
|     2      |  |
+------------+--+
"""
# View port for the map presentation 50 x 45
VIEW_PORT_X = 0
VIEW_PORT_Y = 0
VIEW_PORT_WIDTH = CONSOLE_WIDTH - 20
VIEW_PORT_HEIGHT = CONSOLE_HEIGHT - 5
# Player states 28 x 6 giving space to 6 states (Health, Energy, ...)
STATE_PORT_X = VIEW_PORT_WIDTH + 1
STATE_PORT_Y = 2
STATE_PORT_WIDTH = CONSOLE_WIDTH - VIEW_PORT_WIDTH - 2
STATE_PORT_HEIGHT = 6
# World port for the world and map information
WORLD_PORT_X = VIEW_PORT_WIDTH + 1
WORLD_PORT_Y = 0
WORLD_PORT_WIDTH = CONSOLE_WIDTH - VIEW_PORT_WIDTH - 2
WORLD_PORT_HEIGHT = 1
# Message port for the in game messages
MESSAGE_PORT_X = 1
MESSAGE_PORT_Y = VIEW_PORT_HEIGHT + 1
MESSAGE_PORT_WIDTH = VIEW_PORT_WIDTH - 2
MESSAGE_PORT_HEIGHT = CONSOLE_HEIGHT - MESSAGE_PORT_Y

""" General configuration """
APP_TITLE = "Endless Worlds, 2025 - A multiplayer multiworld roguelike"
APP_AUTHOR = "John Aage Andersen, Latvia"
APP_CONTACT = "j.andersen.lv@gmail.com"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
