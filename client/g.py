""" This module stores globally mutable variables used by this program """

from __future__ import annotations

import tcod.console
import tcod.context
import tcod.ecs

import game.state

""" The window managed by tcod """
context: tcod.context.Context

""" The active ECS registry and current session """
world: tcod.ecs.Registry

""" A stack of states with the last item being the active state """
states: list[game.state.State] = []

""" The current main console """
console: tcod.console.Console