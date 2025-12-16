import numpy as np

graphic_dt = np.dtype(
	[
		("ch", np.int32), # Unicode codepoint
		("fg", "4B"), # 3 unsigned bytes, foreground RGB colours
		("bg", "4B"), # Background RGB colours
	]
)

tile_dt = np.dtype(
	[
		("walkable", bool), # True if walkable tile
		("transparent", bool), # True if tile doesn't block FOV
		("dark", graphic_dt), # Graphics outside of FOV
		("light", graphic_dt), # Graphics inside of FOV
		("gateway", bool), # Gateway if true
	]
)

blank = np.array((True, True, (ord(","), (0, 192, 192, 255), (0, 0, 0, 0)),(ord(","), (0, 192, 192, 255), (0, 0, 0, 0)), False), dtype=tile_dt)

SHROUD = np.array((ord(" "), (255, 255, 255, 255), (0, 0, 0, 0)), dtype=graphic_dt)