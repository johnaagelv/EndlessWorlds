""" This module stores globally mutable variables used by this program """
from __future__ import annotations
import tcod.console
import tcod.context
import tcod.ecs
import selectors

import client.game.state

context: tcod.context.Context
""" The window managed by tcod """

game: tcod.ecs.Registry
""" The active ECS registry and current session """

states: list[client.game.state.State] = []
""" A stack of states with the last item being the active state """

console: tcod.console.Console
""" The active console """

sel = selectors.DefaultSelector()
""" The active selector for communicating with a server """