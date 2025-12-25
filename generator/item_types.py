from __future__ import annotations

#from typing import Tuple
from client.ui.item_tiles import item_faces, item_types

items: dict = {}

def new_item(
	name: str,
	face: int,
	fg: tuple[int, int, int, int],
	bg: tuple[int, int, int, int],
) -> dict:
	return {"name": name, "face": face, "fg": fg, "bg": bg}

for item_face in item_faces:
	items[item_types[item_face]["name"]] = item_types[item_face]
