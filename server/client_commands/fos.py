from __future__ import annotations
from worlds import TWorld

def cmd_fos(request: dict, world: TWorld) -> dict:
	return world.field_of_sense(request, False)
