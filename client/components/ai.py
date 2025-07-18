from __future__ import annotations

from typing import List, Tuple

import numpy as np
import tcod

from actions import TAction
from components.components import TBaseComponent

class TBaseAI(TAction, TBaseComponent):
	def perform(self) -> None:
		raise NotImplementedError()
	
	def get_path(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
#		cost = np.array(self.entity.world.tiles["walkable"], dtype=np.int8)
		return [(0, 0)]