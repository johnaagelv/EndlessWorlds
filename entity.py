from __future__ import annotations

import copy
import math
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union

from render_order import RenderOrder

if TYPE_CHECKING:
	from components.ai import TBaseAI
	from components.consumable import TConsumable
	from components.fighter import TFighter
	from components.inventory import TInventory
	from game_map import TGameMap

T = TypeVar("T", bound="TEntity")


class TEntity:
	"""
	A generic object to represent players, enemies, items, etc.
	"""
	parent: Union[TGameMap, TInventory]

	def __init__(
		self,
		parent: Optional[TGameMap] = None,
		x: int = 0,
		y: int = 0,
		char: str = "?",
		colour: Tuple[int, int, int] = (255, 255, 255),
		name: str = "<Unnamed>",
		blocks_movement: bool = False,
		render_order: RenderOrder = RenderOrder.CORPSE,
	):
		self.x = x
		self.y = y
		self.char = char
		self.colour = colour
		self.name = name
		self.blocks_movement = blocks_movement
		self.render_order = render_order
		if parent:
			# If parent isn't provided now then it will be set later.
			self.parent = parent
			parent.entities.add(self)
		
	@property
	def gamemap(self) -> TGameMap:
		return self.parent.gamemap

	def spawn(self: T, gamemap: TGameMap, x: int, y: int) -> T:
		"""Spawn a copy of this instance at the given location."""
		clone = copy.deepcopy(self)
		clone.x = x
		clone.y = y
		clone.parent = gamemap
		gamemap.entities.add(clone)
		return clone

	def place(self, x: int, y: int, gamemap: Optional[TGameMap] = None) -> None:
		"""Place this entitiy at a new location.  Handles moving across GameMaps."""
		self.x = x
		self.y = y
		if gamemap:
			if hasattr(self, "parent"):  # Possibly uninitialized.
				if self.parent is self.gamemap:
					self.gamemap.entities.remove(self)
			self.parent = gamemap
			gamemap.entities.add(self)

	def distance(self, x: int, y: int, gamemap: Optional[TGameMap] = None) -> None:
		"""
		Return the distance between the current entity and the given (x, y)
		"""
		return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

	def move(self, dx: int, dy: int) -> None:
		# Move the entity by a given amount
		self.x += dx
		self.y += dy


class TActor(TEntity):
	def __init__(
		self,
		*,
		x: int = 0,
		y: int = 0,
		char: str = "?",
		colour: Tuple[int, int, int] = (255, 255, 255),
		name: str = "<Unnamed>",
		ai_cls: Type[TBaseAI],
		fighter: TFighter,
		inventory: TInventory,
	):
		super().__init__(
			x=x,
			y=y,
			char=char,
			colour=colour,
			name=name,
			blocks_movement=True,
			render_order=RenderOrder.ACTOR,
		)

		self.ai: Optional[TBaseAI] = ai_cls(self)

		self.fighter = fighter
		self.fighter.parent = self

		self.inventory = inventory
		self.inventory.parent = self

	@property
	def is_alive(self) -> bool:
		"""
		Returns True as long as this actor can perform actions
		"""
		return bool(self.ai)

class TItem(TEntity):
	def __init__(self, *, x: int=0, y: int=0, char: str="?", colour: Tuple[int, int, int]=(255,255,255), name: str="<Unnamed>", consumable: TConsumable,):
		super().__init__(x=x, y=y, char=char, colour=colour, name=name, blocks_movement=False, render_order=RenderOrder.ITEM)
		self.consumable = consumable
		self.consumable.parent = self