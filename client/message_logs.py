from __future__ import annotations
from typing import List, Tuple, Reversible
import textwrap
import tcod.console
import colours

class TLogMessage:
	def __init__(self, text: str, fg: Tuple[int, int, int]):
		self.plain_text = text
		self.fg = fg
		self.count = 1

	@property
	def full_text(self) -> str:
		if self.count > 1:
			return f"{self.plain_text} (x{self.count})"
		return self.plain_text

class TMessageLog:
	def __init__(self) -> None:
		self.messages: List[TLogMessage] = []
	
	def add(self, text: str, fg: Tuple[int, int, int] = colours.white, *, stack: bool = True) -> None:
		if stack and self.messages and text == self.messages[-1].plain_text:
			self.messages[-1].count += 1
		else:
			self.messages.append(TLogMessage(text, fg))

	def render(self, console: tcod.console.Console, x: int, y: int, width: int, height: int) -> None:
		self.render_messages(console, x, y, width, height, self.messages)

	@staticmethod
	def render_messages(console: tcod.console.Console, x: int, y: int, width: int, height: int, messages: Reversible[TLogMessage]) -> None:
		y_offset = height - 1
		for message in reversed(messages):
			for line in reversed(textwrap.wrap(message.full_text, width)):
				console.print(x=x, y=y+y_offset, text=line, fg=message.fg)
				y_offset -= 1
				if y_offset < 0:
					return
