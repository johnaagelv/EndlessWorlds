from entities import TActor

from worlds import TWorld

class TAction:
	pass

class TEscapeAction(TAction):
	def run(self, player: TActor):
		player.data["playing"] = False

class TMoveAction(TAction):
	def __init__(self, dx: int, dy: int):
		super().__init__()
		self.dx = dx
		self.dy = dy

	def run(self, player: TActor):
		world: TWorld = player.data["world"]
		map = world.maps[player.data["m"]]
		dest_x = player.data["x"] + self.dx
		dest_y = player.data["y"] + self.dy

		# Check in bounds of the map
		if 0 <= dest_x < map["width"] and 0 <= dest_y < map["height"]:
			# Check if walkable
			if map["tiles"]["walkable"][dest_x, dest_y]:
				if world.in_gateway(dest_x, dest_y, player.data["m"]):
					gateway = world.go_gateway(dest_x, dest_y, player.data["m"])
					# Move to x, y coordinate in map number m
					player.data["x"] = gateway["x"]
					player.data["y"] = gateway["y"]
					player.data["m"] = gateway["m"]
				else:
					# Move to x, y coordinate
					player.data["x"] = dest_x
					player.data["y"] = dest_y