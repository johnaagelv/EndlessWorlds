""" UI configuration """

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
VIEW_PORT_WIDTH = CONSOLE_WIDTH - 20
VIEW_PORT_HEIGHT = CONSOLE_HEIGHT - 5
# 2: Message view port
MESSAGE_PORT_X = 1
MESSAGE_PORT_Y = VIEW_PORT_HEIGHT + 1
MESSAGE_PORT_WIDTH = VIEW_PORT_WIDTH - 2
MESSAGE_PORT_HEIGHT = CONSOLE_HEIGHT - MESSAGE_PORT_Y
# 3: World view port
WORLD_PORT_X = VIEW_PORT_WIDTH + 1
WORLD_PORT_Y = 0
WORLD_PORT_WIDTH = CONSOLE_WIDTH - VIEW_PORT_WIDTH - 2
WORLD_PORT_HEIGHT = 1
# 4: Player states 28 x 6 giving space to 6 states (Health, Energy, ...)
STATE_PORT_X = VIEW_PORT_WIDTH + 1
STATE_PORT_Y = 2
STATE_PORT_WIDTH = CONSOLE_WIDTH - VIEW_PORT_WIDTH - 2
STATE_PORT_HEIGHT = 6
