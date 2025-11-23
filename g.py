""" This module stores globally mutable variables used by this program """
from __future__ import annotations

#from typing import List
import tcod.console
import tcod.context
import tcod.ecs

#import game.state
#from game.components import MessageLog

""" The window managed by tcod """
context: tcod.context.Context

""" The active ECS registry and current session """
world: tcod.ecs.Registry

""" A stack of states with the last item being the active state """
states: list[game.state.State] = []

""" The current main console """
console: tcod.console.Console

""" Message log """
messages: MessageLog

""" Game title and author """
GAME_TITLE = "Endless Worlds, 2025"
GAME_AUTHOR = "John Aage Andersen, Latvia"

""" Game tileset to use """
GAME_TILESET_FILENAME = "client/redjack17.png"

""" Log file configuration """
LOG_FILENAME = "EWclient.log"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"

""" Screen size """
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

""" Game viewport size and location """
GAME_VIEWPORT_WIDTH = SCREEN_WIDTH - 20
GAME_VIEWPORT_HEIGHT = SCREEN_HEIGHT - 10
GAME_VIEWPORT_X = 0
GAME_VIEWPORT_Y = 0

""" Messages viewport size and location """
MESSAGES_VIEWPORT_HEIGHT = 6
MESSAGES_VIEWPORT_WIDTH = GAME_VIEWPORT_WIDTH
MESSAGES_VIEWPORT_X = 1
MESSAGES_VIEWPORT_Y = SCREEN_HEIGHT - MESSAGES_VIEWPORT_HEIGHT - 1
