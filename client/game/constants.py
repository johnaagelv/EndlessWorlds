""" Constants used in the game """
from __future__ import annotations

from typing import Final

from tcod.event import KeySym

DIRECTION_KEYS: Final = {
	# Arrow keys
	KeySym.LEFT: (-1, 0), # left
	KeySym.RIGHT: (1, 0), # right
	KeySym.UP: (0, -1), # up
	KeySym.DOWN: (0, 1), # down
	KeySym.HOME: (-1, -1), # left up
	KeySym.END: (-1, 1), # left down
	KeySym.PAGEUP: (1, -1), # right up
	KeySym.PAGEDOWN: (1, 1), # right down
	# Keypad keys
	KeySym.KP_4: (-1, 0), # left
	KeySym.KP_6: (1, 0), # right
	KeySym.KP_8: (0, -1), # up
	KeySym.KP_2: (0, 1), # down
	KeySym.KP_7: (-1, -1), # left up
	KeySym.KP_1: (-1, 1), # left down
	KeySym.KP_9: (1, -1), # right up
	KeySym.KP_3: (1, 1), # right down
	# VI keys
	KeySym.H: (-1, 0), # left
	KeySym.L: (1, 0), # right
	KeySym.K: (0, -1), # up
	KeySym.J: (0, 1), # down
	KeySym.Y: (-1, -1), # left up
	KeySym.B: (-1, 1), # left down
	KeySym.U: (1, -1), # right up
	KeySym.N: (1, 1), # right down
}