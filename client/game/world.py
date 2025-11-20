""" World manager """
from __future__ import annotations

import numpy as np

# Each map conform to this template
map_template: dict = {
	"loaded": bool,
	"width": int,
	"height": int,
	"tiles": np.ndarray,
	"visible": np.ndarray,
	"explored": np.ndarray,
	"gateways": list
}

class World:
	maps: list[dict] = []
