""" UI configuration """
from __future__ import annotations


"""
UI layout - 1: Map; 2: Messages; 3: World information; 4: Player states
+-----------------+---+
|                 | 3 |
|        1        +---+
|                 | 4 |
+-----------------+---+
|        2        | 5 |
+-----------------+---+
"""
# 0: Console
CONSOLE_WIDTH = 110
CONSOLE_HEIGHT = 60
BORDER = 1 # Border of size 1 between all areas
# 1: Map view port
VIEW_PORT_X = BORDER - 1
VIEW_PORT_Y = BORDER - 1
VIEW_PORT_WIDTH = 88
VIEW_PORT_HEIGHT = 40
# 2: Message view port
MESSAGE_PORT_X = BORDER
MESSAGE_PORT_Y = VIEW_PORT_Y + VIEW_PORT_HEIGHT + BORDER
MESSAGE_PORT_WIDTH = VIEW_PORT_WIDTH
MESSAGE_PORT_HEIGHT = 10
# 3: World view port
WORLD_PORT_WIDTH = 20
WORLD_PORT_X = max(CONSOLE_WIDTH - WORLD_PORT_WIDTH - BORDER * 2, VIEW_PORT_X + VIEW_PORT_WIDTH - WORLD_PORT_WIDTH - BORDER * 2) + BORDER
WORLD_PORT_Y = 0
WORLD_PORT_HEIGHT = 2
# 4: Player states 28 x 6 giving space to 6 states (Health, Energy, ...)
STATE_PORT_WIDTH = WORLD_PORT_WIDTH
STATE_PORT_X = max(CONSOLE_WIDTH - WORLD_PORT_WIDTH - BORDER * 2, VIEW_PORT_X + VIEW_PORT_WIDTH - STATE_PORT_WIDTH - BORDER * 2) + BORDER
STATE_PORT_Y = WORLD_PORT_Y + WORLD_PORT_HEIGHT + BORDER
STATE_PORT_HEIGHT = 8
