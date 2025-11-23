""" Global client constants """
from __future__ import annotations
from typing import Final
from tcod.event import KeySym

DIRECTION_KEYS: Final = {
	# Arrow keys
	KeySym.LEFT: (-1, 0), # North
	KeySym.RIGHT: (1, 0), # South
	KeySym.UP: (0, -1), # West
	KeySym.DOWN: (0, 1), # East
	KeySym.HOME: (-1, -1), # North west
	KeySym.END: (-1, 1), # North east
	KeySym.PAGEUP: (1, -1), # South west
	KeySym.PAGEDOWN: (1, 1), # South east
	# KeyPad
	KeySym.KP_4: (-1, 0), # North
	KeySym.KP_6: (1, 0), # South
	KeySym.KP_8: (0, -1), # West
	KeySym.KP_2: (0, 1), # East
	KeySym.KP_7: (-1, -1), # North west
	KeySym.KP_1: (-1, 1), # North east
	KeySym.KP_9: (1, -1), # South west
	KeySym.KP_3: (1, 1), # South east
	# VI keys
	KeySym.H: (-1, 0), # North
	KeySym.L: (1, 0), # South
	KeySym.K: (0, -1), # West
	KeySym.J: (0, 1), # East
	KeySym.Y: (-1, -1), # North west
	KeySym.B: (-1, 1), # North east
	KeySym.U: (1, -1), # South west
	KeySym.N: (1, 1), # South east
	# Idle
	KeySym.PERIOD: (0, 0), # Wait
}

ACTION_KEYS: Final = {
	KeySym.Q: ord("q"), # 
	KeySym.W: ord("w"), # Wear/wield
	KeySym.E: ord("e"), # Eat
	KeySym.R: ord("r"), # Remove
	KeySym.T: ord("t"), # 
	KeySym.I: ord("i"), # Inventory
	KeySym.O: ord("o"), # 
	KeySym.P: ord("p"), # 
	KeySym.A: ord("a"), # Activate
	KeySym.S: ord("s"), # 
	KeySym.D: ord("d"), # Drink
	KeySym.F: ord("f"), # 
	KeySym.G: ord("g"), # 
	KeySym.Z: ord("z"), # 
	KeySym.X: ord("x"), # 
	KeySym.C: ord("c"), # 
	KeySym.V: ord("v"), # 
	KeySym.M: ord("m"), # 
	KeySym.COMMA: ord(","), # Pick up
	KeySym.LESS: ord("<"), # Down
	KeySym.GREATER: ord(">"), # Up
	KeySym.N1: ord("1"), # Lift floor 1
	KeySym.N2: ord("2"), # Lift floor 2
	KeySym.N3: ord("3"), # Lift floor 3
	KeySym.N4: ord("4"), # Lift floor 4
	KeySym.N5: ord("5"), # Lift floor 5
	KeySym.N6: ord("6"), # Lift floor 6
	KeySym.N7: ord("7"), # Lift floor 7
	KeySym.N8: ord("8"), # Lift floor 8
	KeySym.N9: ord("9"), # Lift floor 9
	KeySym.LEFTBRACKET: ord("["), #
	KeySym.RIGHTBRACKET: ord("]"), #
	KeySym.LEFTBRACE: ord("{"), #
	KeySym.RIGHTBRACE: ord("}"), #
	KeySym.LEFTPAREN: ord("("), #
	KeySym.RIGHTPAREN: ord(")"), #
	KeySym.SEMICOLON: ord(";"), #
	KeySym.COLON: ord(":"), #
	KeySym.APOSTROPHE: ord("!"), #
	KeySym.AT: ord("@"), #
	KeySym.ASTERISK: ord("*"), #
	KeySym.DOLLAR: ord("$"), #
	KeySym.HASH: ord("#"), #
	KeySym.PERCENT: ord("%"), #
	KeySym.AMPERSAND: ord("&"), #
	KeySym.CARET: ord("^"), #
	KeySym.UNDERSCORE: ord("_"), #
	KeySym.EQUALS: ord("="), #
	KeySym.PLUS: ord("+"), #
	KeySym.MINUS: ord("-"), #
	KeySym.TILDE: ord("~"), #
	KeySym.SLASH: ord("/"), #
	KeySym.BACKSLASH: ord("\\"), #
	KeySym.PIPE: ord("|"), #
	KeySym.QUESTION: ord("?"), #
}