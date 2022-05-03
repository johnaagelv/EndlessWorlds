import tcod

class TUiController:
	def __init__(self, x: int, y: int, width: int, height: int):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def present(self, console: tcod.Console, text: str) -> None:
		pass