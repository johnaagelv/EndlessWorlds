""" Tools used to manage states in the game """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

import tcod.event

import g
from game.state import State, StateResult, Push, Pop, Reset

""" Global draw of states """
def main_draw() -> None:
	logger.info('main_draw() -> None')
	if not g.states:
		return
	g.console.clear()
	g.states[-1].on_draw(g.console)
	g.context.present(g.console)

""" Apply state result to g.states """
def apply_state_result(result: StateResult) -> None:
	logger.info("apply_state_result( result: StateResult ) -> None")
	match result:
		case Push(state=state):
			g.states.append(state)
		case Pop():
			g.states.pop()
		case Reset(state=state):
			while g.states:
				apply_state_result(Pop())
			apply_state_result(Push(state))
		case None:
			pass
		case _:
			raise TypeError(result)

""" Run the active state forever """
def main_loop() -> None:
	logger.info("main_loop() -> None")
	while g.states:
		main_draw()
		for event in tcod.event.wait():
			tile_event = g.context.convert_event(event)
			if g.states:
				apply_state_result(g.states[-1].on_event(tile_event))

""" Return the state before the state in the stack if exists """
def get_previous_state(state: State) -> State | None:
	logger.info("get_previous_state( state: State ) -> State | None")
	current_index = next(index for index, value in enumerate(g.states) if value is state)
	return g.states[current_index - 1] if current_index > 0 else None

""" Previous states to be drawn """
def draw_previous_state(state: State, console: tcod.console.Console, dim: bool = True) -> None:
	logger.info("draw_previous_state( state: State, console: tcod.console.Console, dim: bool = True ) -> None")
	prev_state = get_previous_state(state)
	if prev_state is None:
		logger.info("- no previous state")
		return
	
	prev_state.on_draw(console)

	if dim and state is g.states[-1]:
		console.rgb["fg"] //= 4
		console.rgb["bg"] //= 4