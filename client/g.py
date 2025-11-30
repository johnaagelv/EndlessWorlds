""" This module stores globally mutable variables used by this program """
from __future__ import annotations
import tcod.console
import tcod.context
import tcod.ecs
import selectors
from tcod.ecs import Registry

import client.ui.configuration as ui

import client.game.state

context: tcod.context.Context
""" The window managed by tcod """

game: tcod.ecs.Registry = Registry()
""" The active ECS registry and current session """

states: list[client.game.state.State] = []
""" A stack of states with the last item being the active state """

console: tcod.console.Console = tcod.console.Console(ui.CONSOLE_WIDTH, ui.CONSOLE_HEIGHT, order="F")
""" The active console """

sel = selectors.DefaultSelector()
""" The active selector for communicating with a server """