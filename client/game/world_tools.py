""" World tools to manage the ECS registry """
from __future__ import annotations
import logging
logger = logging.getLogger("EWClient")

from random import Random
from tcod.ecs import Registry
import game.components as gc
from game.tags import IsActor, IsItem, IsPlayer, IsContainer, IsInventory

import numpy as np
import tile_types
import colours

def new_world() -> Registry:
	logger.info("new_world() -> Registry")
	registry = Registry()

	""" Register a random number generator """
	rng = registry[None].components[Random] = Random()

	world = registry[object()]

	npc = registry[object()]
	npc.components[gc.Position] = gc.Position(15, 5)
	npc.components[gc.Graphic] = gc.Graphic(9787)
	npc.tags |= {IsActor}

	player = registry[object()]
	player.components[gc.Position] = gc.Position(5, 5)
	player.components[gc.Graphic] = gc.Graphic(ord("@"))
	player.components[gc.Health] = gc.Health(240000, 62500, 125000, 250000)
	player.components[gc.HealthImpacts] = gc.HealthImpacts(-100, -50, -1, [gc.Strength, gc.Energy])
	player.components[gc.Energy] = gc.Energy(240000, 62500, 125000, 250000)
	player.components[gc.EnergyUsage] = gc.EnergyUsage(-100)
	player.components[gc.EnergyImpacts] = gc.EnergyImpacts(-100, -50, -1, [gc.Strength, gc.Health])
	player.components[gc.Strength] = gc.Strength(500000, 62500, 125000, 250000)
	player.components[gc.StrengthImpacts] = gc.StrengthImpacts(-10, -5, -1, [gc.Energy, gc.Health])
	player.components[gc.Gold] = gc.Gold(1)
	player.components[gc.IsA] = gc.IsA("Gold")

	inventory = Registry()
	player.components[gc.Inventory] = gc.Inventory(inventory, 8)
#	equipment = registry[object()]
#	equipment.tags |= {IsContainer}
#	player.components[gc.Equipment] = gc.Equipment(equipment, 8)

	player.tags |= {IsPlayer}

	world.components[gc.ExplorationMemory] = gc.ExplorationMemory(
		np.full((80, 50), fill_value=tile_types.blank, order="F"),
		np.full((80, 50), fill_value=False, order="F"),
		np.full((80, 50), fill_value=False, order="F"),
		[]
	)

	for _ in range(rng.randint(6,12)):
		valuable = registry[object()]
		valuable.components[gc.IsA] = gc.IsA("Gold")
		valuable.components[gc.Position] = gc.Position(rng.randint(0, 10), rng.randint(0, 25))
		valuable.components[gc.Graphic] = gc.Graphic(ord("$"), fg=(255, 255, 0))
		valuable.components[gc.Gold] = gc.Gold(rng.randint(1, 10))
		valuable.components[gc.StatsImpacts] = gc.StatsImpacts([gc.Gold])
		valuable.tags |= {IsItem}

	for _ in range(rng.randint(12,22)):
		valuable = registry[object()]
		valuable.components[gc.IsA] = gc.IsA("Food")
		valuable.components[gc.Position] = gc.Position(rng.randint(0, 60), rng.randint(0, 35))
		valuable.components[gc.Graphic] = gc.Graphic(9576, fg=colours.lightgoldenrodyellow)
		valuable.components[gc.Food] = gc.Food(rng.randint(1000, 50000))
		valuable.components[gc.StatsImpacts] = gc.StatsImpacts([gc.Energy])
		valuable.tags |= {IsItem}

	return registry