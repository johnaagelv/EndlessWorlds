""" Global client constants """
from __future__ import annotations
from typing import Final
from tcod.event import KeySym, Modifier

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

STAIR_KEYS: Final = {
	(KeySym.COMMA, Modifier.LSHIFT): "up",
	(KeySym.COMMA, Modifier.RSHIFT): "up",
	(KeySym.PERIOD, Modifier.LSHIFT): "down",
	(KeySym.PERIOD, Modifier.RSHIFT): "down",
}

ACTION_KEYS: Final = {
	(KeySym.Q, Modifier.NONE): ord("q"), # 
	(KeySym.W, Modifier.NONE): ord("w"), # Wear/wield
	(KeySym.E, Modifier.NONE): ord("e"), # Eat
	(KeySym.R, Modifier.NONE): ord("r"), # Remove
	(KeySym.T, Modifier.NONE): ord("t"), # 
	(KeySym.I, Modifier.NONE): ord("i"), # Inventory
	(KeySym.O, Modifier.NONE): ord("o"), # 
	(KeySym.P, Modifier.NONE): ord("p"), # 
	(KeySym.A, Modifier.NONE): ord("a"), # Activate
	(KeySym.S, Modifier.NONE): ord("s"), # 
	(KeySym.D, Modifier.NONE): ord("d"), # Drink
	(KeySym.F, Modifier.NONE): ord("f"), # 
	(KeySym.G, Modifier.NONE): ord("g"), # 
	(KeySym.Z, Modifier.NONE): ord("z"), # 
	(KeySym.X, Modifier.NONE): ord("x"), # 
	(KeySym.C, Modifier.NONE): ord("c"), # 
	(KeySym.V, Modifier.NONE): ord("v"), # 
	(KeySym.M, Modifier.NONE): ord("m"), # 
	(KeySym.COMMA, Modifier.NONE): ord(","), # Pick up
	(KeySym.N1, Modifier.NONE): ord("1"), # Lift floor 1
	(KeySym.N2, Modifier.NONE): ord("2"), # Lift floor 2
	(KeySym.N3, Modifier.NONE): ord("3"), # Lift floor 3
	(KeySym.N4, Modifier.NONE): ord("4"), # Lift floor 4
	(KeySym.N5, Modifier.NONE): ord("5"), # Lift floor 5
	(KeySym.N6, Modifier.NONE): ord("6"), # Lift floor 6
	(KeySym.N7, Modifier.NONE): ord("7"), # Lift floor 7
	(KeySym.N8, Modifier.NONE): ord("8"), # Lift floor 8
	(KeySym.N9, Modifier.NONE): ord("9"), # Lift floor 9
	(KeySym.LEFTBRACKET, Modifier.NONE): ord("["), #
	(KeySym.RIGHTBRACKET, Modifier.NONE): ord("]"), #
	(KeySym.SEMICOLON, Modifier.NONE): ord(";"), #
	(KeySym.EQUALS, Modifier.NONE): ord("="), #
	(KeySym.MINUS, Modifier.NONE): ord("-"), #
	(KeySym.SLASH, Modifier.NONE): ord("/"), #
	(KeySym.BACKSLASH, Modifier.NONE): ord("\\"), #
}