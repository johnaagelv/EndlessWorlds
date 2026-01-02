""" UI configuration """
from __future__ import annotations

CONSOLE_WIDTH = 80
CONSOLE_HEIGHT = 50

"""
UI layout - 1: Map; 2: Messages; 3: World information; 4: Player states
+-----------------+---+
|                 | 3 |
|        1        | 4 |
|                 |   |
+-----------------+   |
|        2        |   |
+-----------------+---+
"""
# 1: Map view port 50 x 45
VIEW_PORT_X = 0
VIEW_PORT_Y = 0
VIEW_PORT_WIDTH = 50
VIEW_PORT_HEIGHT = 45
# 2: Message view port
MESSAGE_PORT_X = 1
MESSAGE_PORT_Y = VIEW_PORT_HEIGHT + 1
MESSAGE_PORT_WIDTH = VIEW_PORT_WIDTH - 2
MESSAGE_PORT_HEIGHT = CONSOLE_HEIGHT - MESSAGE_PORT_Y
# 3: World view port
WORLD_PORT_BORDER = 1
WORLD_PORT_WIDTH = 20
WORLD_PORT_X = max(CONSOLE_WIDTH - WORLD_PORT_WIDTH - WORLD_PORT_BORDER * 2, VIEW_PORT_X + VIEW_PORT_WIDTH - WORLD_PORT_WIDTH - WORLD_PORT_BORDER * 2) + WORLD_PORT_BORDER
WORLD_PORT_Y = 0
WORLD_PORT_HEIGHT = 1
# 4: Player states 28 x 6 giving space to 6 states (Health, Energy, ...)
STATE_PORT_BORDER = WORLD_PORT_BORDER
STATE_PORT_WIDTH = WORLD_PORT_WIDTH
STATE_PORT_X = max(CONSOLE_WIDTH - WORLD_PORT_WIDTH - STATE_PORT_BORDER * 2, VIEW_PORT_X + VIEW_PORT_WIDTH - STATE_PORT_WIDTH - STATE_PORT_BORDER * 2) + STATE_PORT_BORDER
STATE_PORT_Y = WORLD_PORT_Y + WORLD_PORT_HEIGHT + STATE_PORT_BORDER
STATE_PORT_HEIGHT = 6
