from typing import List, Tuple
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
