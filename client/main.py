"""
Client, implements the player
- Startup play
- Run player
- Shutdown play
"""
from TActors import TActor
from TPlayControllers import TPlayStartup, TPlayShutdown

def main():
	# Startup with an empty player
	player = TActor()
	if TPlayStartup().run(player):
		# Play while the player wants to/can play
		while player.is_playing:
			player.run()

	# Shutdown the player
	TPlayShutdown().run(player)

if __name__ == '__main__':
	main()