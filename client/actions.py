class TAction:
	pass

class TEscapeAction(TAction):
	pass

class TMoveAction(TAction):
	def __init__(self, dx: int, dy: int):
		super().__init__()
		self.dx = dx
		self.dy = dy