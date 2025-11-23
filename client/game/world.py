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

	def start_map(self, map_idx):
	#	logger.info(f"TWorld->start_map( map_idx={map_idx} )")
		map_idx = self.actor.map_idx
	#	logger.info(f"- switch to map_idx={map_idx}")
		if self.maps[map_idx]['loaded'] == False:
	#		logger.info(f" - loading map definition")
			map_definition = self.map_definitions[map_idx]

			map_name = map_definition.get('name')
			map_width = int(map_definition.get("width"))
			map_height = int(map_definition.get("height"))
			map_visible = map_definition.get('visible')
			self.maps[map_idx] = {
				"loaded": True,
				"name": map_name,
				"width": map_width,
				"height": map_height,
				"tiles": np.full((map_width, map_height), fill_value=tile_types.blank, order="F"),
				"visible": np.full((map_width, map_height), fill_value=map_visible, order="F"),
				"explored": np.full((map_width, map_height), fill_value=map_visible, order="F"),
			}

			if map_visible:
				fos = map_definition.get("fos")
				temp = fos.get("view")
				view = np.array(temp)
				if self.maps[map_idx] is not None:
					current_map = self.maps[map_idx]
					if current_map is not None:
						current_map["tiles"][0:map_width, 0:map_height] = view
