from __future__ import annotations
from typing import TYPE_CHECKING
import colours as colour

if TYPE_CHECKING:
	from tcod import console

def render_bar(
	console: Console,
	value: int,
	max_value: int,
	width: int
) -> None:
	bar_width = int(float(value) / max_value * width)
	console.draw_rect(x=0, y=45, width=width, height=1, ch=1, bg=colour.bar_empty)

	if bar_width > 0:
		console.draw_rect(x=0, y=45, width=bar_width, height=1, ch=1, bg=colour.bar_filled)
	
	console.print(x=1, y=45, string=f"HP: {value}/{max_value}", fg=colour.bar_text)