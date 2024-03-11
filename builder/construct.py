import math

def build_entryway(map, item):
	x = item["x"]
	y = item["y"]
	w = item["w"]
	h = item["h"]
	outer = item["outer"]
	map[x, y] = outer

def build_circle_wall(map, item):
	x = item["x"] # x coordinate of circle center
	y = item["y"] # y coordinate of circle center
	r = item["r"] # circle radius
	t = item.get('t') # circle thickness
	if t is None:
		t = 1
	t = min(t, r)
	outer = item["outer"]
	for d in range(0, t):
		for a in range(0, 360):
			rx = int(math.sin(a) * (r - d)) + x
			ry = int(math.cos(a) * (r - d)) + y
			map[rx, ry] = outer
#			rx = int(math.sin(a) * (r - 1)) + x
#			ry = int(math.cos(a) * (r - 1)) + y
#			map[rx, ry] = outer

def build_circle(map, item):
	x = item["x"]
	y = item["y"]
	r = item["r"]
	outer = item["outer"]
	for a in range(0, 360):
		rx = int(math.sin(a) * r) + x
		ry = int(math.cos(a) * r) + y
		map[rx, ry] = outer

def build_square(map, item):
	x = item["x"]
	y = item["y"]
	w = item["w"]
	h = item["h"]
	outer = item.get('outer')
	inner = item.get('inner')

	map[x:x + w, y:y + h] = outer
	if inner is not None:
		map[x + 1:x + w - 1, y + 1:y + h - 1] = inner
