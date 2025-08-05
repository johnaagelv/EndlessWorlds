""" This module contains the collection of systems in the game """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

import tcod.event
import g
from game.states import StateResult, State
from game.state import Push, Pop, Reset
from game.tags import IsPlayer
from game.components import Health, HealthImpacts, Energy, EnergyImpacts, Strength, StrengthImpacts

from tile_types import SHROUD

""" Global draw of states """
def main_draw() -> None:
	logger.info('main_draw() -> None')
	if not g.states:
		return
	g.console.clear()
	g.states[-1].on_draw(g.console)
	g.context.present(g.console)

""" Affects other states """
def apply_impact(main_state, impact_state):
	if g.world is not None:
		(player,) = g.world.Q.all_of(tags=[IsPlayer])
		energy = player.components[main_state]
		impacts = player.components[impact_state]
		for affected_state in impacts.impacts:
			if player.components[affected_state].value > energy.value:
				affected_impact = (0 <= energy.value < energy.low) * impacts.low + (energy.low <= energy.value < energy.medium) * impacts.medium + (energy.medium <= energy.value < energy.high) * impacts.high
				player.components[affected_state] += affected_impact

""" Global input of states """
def main_input() -> None:
	for event in tcod.event.wait(timeout=0.1):
		tile_event = g.context.convert_event(event)
		if g.states:
			apply_state_result(g.states[-1].on_event(tile_event))

""" Apply state result to g.states """
def apply_state_result(result: StateResult) -> None:
	logger.info("apply_state_result( result: StateResult ) -> None")
	match result:
		case Push(state=state):
			# Append a new state to g.states
			g.states.append(state)
		case Pop():
			# Remove the current state if any
			g.states.pop()
		case Reset(state=state):
			# Remove all states from g.states and replace with the specified state
			while g.states:
				apply_state_result(Pop())
			apply_state_result(Push(state))
		case None:
			pass
		case _:
			raise TypeError(result)

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
		console.rgb["fg"] //= 2
		console.rgb["bg"] //= 2
