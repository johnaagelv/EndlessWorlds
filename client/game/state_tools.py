""" Module will handle rendering of the global state """
from __future__ import annotations

import client.g as g
import tcod.event

from client.game.state import Push, Pop, Reset, State, StateResult
from client.game.components import Map, Position, Vision, World
from client.game.tags import IsPlayer, IsWorld

import client.game.connect_tools
import client.configuration as config
import logging
logger = logging.getLogger(config.LOG_NAME_CLIENT)

def main_draw() -> None:
	""" Main draw of the active game state (last in g.states stack) """
	logger.debug("main_draw() -> None")
	if not g.states:
		return
	g.console.clear()
	g.states[-1].on_draw(g.console)
	g.context.present(g.console)

def apply_state_result(result: StateResult) -> None:
	""" Apply a StateResult to the g.states stack """
	logger.debug("apply_state_result( result ) -> None")
	match result:
		case Push(state=state):
			# Switch to a new game state
			g.states.append(state)
		case Pop():
			# Remove current game state
			g.states.pop()
		case Reset(state=state): 
			# Clear the game state stack
			while g.states:
				apply_state_result(Pop())
			# Now activate this state
			apply_state_result(Push(state))
		case None:
			pass
		case _:
			raise TypeError(result)

def main_loop() -> None:
	""" Run the active game state forever """
	logger.debug("main_loop() -> None")
	while g.states:
		main_draw()
		for event in tcod.event.wait():
			tile_event = g.context.convert_event(event)
			if g.states:
				apply_state_result(g.states[-1].on_event(tile_event))
		do_fos_query()

def get_previous_state(state: State) -> State | None:
	""" Return the game state before this state if it exists """
	logger.debug("get_previous_state( state ) -> State")
	current_index = next(index for index, value in enumerate(g.states) if value is state)
	return g.states[current_index - 1] if current_index > 0 else None

def draw_previous_state(state: State, console: tcod.console.Console, dim: bool = True) -> None:
	""" Draw previous states, optionally dimming all but the active state """
	logger.debug("draw_previous_state( state, console, dim ) -> None")
	prev_state = get_previous_state(state)
	if prev_state is None:
		return
	prev_state.on_draw(console)
	if dim and state is g.states[-1]:
		console.rgb["fg"] //= 4
		console.rgb["bg"] //= 4

def do_fos_query() -> None:
	world = g.game.Q.all_of(tags=[IsWorld]).get_entities()
	if len(world) == 0:
		#(player,) = g.game.Q.all_of(tags=[IsPlayer])
		request = {
			"cmd":"fos",
			"cid": "1234", # if CID is not provided, then this is a new actor and will be placed in the world by the server
			"m": 0,
			"x": 10,
			"y": 10,
			"z": 0,
			"r": 4,
		}
		result = client.game.connect_tools.query_server(request)
