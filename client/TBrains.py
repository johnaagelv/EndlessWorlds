from TActions import TAction

class TBrain:
	def __init__(self):
		pass

	def run(self) -> TAction:
		raise NotImplementedError()

class TPlayerBrain(TBrain):
	def run(self) -> TAction:
		action = TAction()
		return action
