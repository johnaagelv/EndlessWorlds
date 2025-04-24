import generate.xtile_types as xtile_types
import math

def type_square(map, tile, x: int, y: int, width: int, height: int, fill: bool):
	# (x, y) is upper left
	# (x + width, y + height) is lower right
	if fill:
		map['tiles'][x:x + width, y:y + height] = xtile_types.tiles[tile]
	else:
		map['tiles'][x, y:y + height] = xtile_types.tiles[tile]
		map['tiles'][x + width - 1, y:y + height] = xtile_types.tiles[tile]
		map['tiles'][x:x + width, y] = xtile_types.tiles[tile]
		map['tiles'][x:x + width, y + height - 1] = xtile_types.tiles[tile]

def type_circle(map, tile, x: int, y: int, radius: int, fill: bool):
	# (x, y) is the center
	# radius is the radius of the circle
	radius_start = radius
	if fill:
		radius_start = 0
	for angle in range(0, 360, 1):
		for r in range(radius_start, radius + 1):
			xr = x + int(math.sin(angle) * r)
			yr = y + int(math.cos(angle) * r)
			map['tiles'][xr, yr] = xtile_types.tiles[tile]
	
# Build definition (name, tile, type, fill, width, height)
def landscape(map, build):
	t = build['tile']
	x = build['x']
	y = build['y']
	w = build['width']
	h = build['height']
	f = build['fill']
	type_square(map, t, x, y, w, h, f)

def fence(map, build):
	t = build['tile']
	x = build['x']
	y = build['y']
	r = build['radius']
	f = build['fill']
	type_circle(map, t, x, y, r, f)
