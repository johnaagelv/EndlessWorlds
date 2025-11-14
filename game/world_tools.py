""" World tools to manage the ECS registry """
from __future__ import annotations
import logging

import time
from random import Random
from tcod.ecs import Registry
import game.components as gc
import game.tags as gt

import numpy as np
import client.tile_types
import ui.colours
logger = logging.getLogger("EWClient")

def new_world() -> Registry:
	logger.info("new_world() -> Registry")
	registry = Registry()

	""" Register a random number generator """
	rng = registry[None].components[Random] = Random()

	""" Define the default player """
	player = registry[object()]
	player.components[gc.Position] = gc.Position(5, 5)
	player.components[gc.Graphic] = gc.Graphic(ord("@"))
	player.components[gc.ActorTimer] = gc.ActorTimer(time.time())
	player.components[gc.Health] = gc.Health(240000, 62500, 125000, 250000)
	player.components[gc.HealthImpacts] = gc.HealthImpacts(-100, -50, -1, [gc.Strength, gc.Energy])
	player.components[gc.Energy] = gc.Energy(240000, 62500, 125000, 250000)
	player.components[gc.EnergyUsage] = gc.EnergyUsage(-100)
	player.components[gc.EnergyImpacts] = gc.EnergyImpacts(-100, -50, -1, [gc.Strength, gc.Health])
	player.components[gc.Strength] = gc.Strength(500000, 62500, 125000, 250000)
	player.components[gc.StrengthImpacts] = gc.StrengthImpacts(-10, -5, -1, [gc.Energy, gc.Health])
	player.components[gc.Gold] = gc.Gold(0, "gold")
	player.tags |= {gt.IsPlayer}

	""" Give the player an inventory """
	inventory = Registry()
	player.components[gc.Inventory] = gc.Inventory(inventory, 8)

	""" Define NPCs incl. some related to the player """
	for _ in range(rng.randint(5,10)):
		npc = registry[object()]
		npc.components[gc.Position] = gc.Position(rng.randint(1, 59), rng.randint(1, 40))
		npc.components[gc.Graphic] = gc.Graphic(9787)
		npc.components[gc.ActorTimer] = gc.ActorTimer(time.time())
#		if rng.randint(0,100) > 40:
#			npc.components[gc.Relationship] = gc.Relationship(player, rng.randint(-9, 9))
		npc.tags |= {gt.IsActor}

	world = registry[object()]
	""" Initialize player memory """
	world.components[gc.ExplorationMemory] = gc.ExplorationMemory(
		np.full((80, 50), fill_value=client.tile_types.blank, order="F"),
		np.full((80, 50), fill_value=False, order="F"),
		np.full((80, 50), fill_value=False, order="F"),
		[] # Gateways
	)

	""" Place some gold on the map """
	for _ in range(rng.randint(1, 10)):
		valuable = registry[object()]
		valuable.components[gc.Position] = gc.Position(rng.randint(1, 59), rng.randint(1, 40))
		valuable.components[gc.Graphic] = gc.Graphic(ord("$"), fg=ui.colours.gold)
		valuable.components[gc.Gold] = gc.Gold(rng.randint(1, 10), "gold")
		valuable.tags |= {gt.IsItem}

	""" Place some food (consumable) on the map """
	for _ in range(rng.randint(1,10)):
		valuable = registry[object()]
		valuable.components[gc.Position] = gc.Position(rng.randint(1, 59), rng.randint(1, 40))
		valuable.components[gc.Graphic] = gc.Graphic(9576, fg=ui.colours.lightgoldenrodyellow)
		valuable.components[gc.Food] = gc.Food(rng.randint(1000, 1234), "food")
		valuable.tags |= {gt.IsItem, gt.IsConsumable}

	return registry