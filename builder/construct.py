import math

def build_accessway(map, item):
	x = item.get('x')
	y = item.get('y')
	outer = item.get('outer')
	actions = item.get('actions')
	map[x, y] = outer

def build_entryway(map, item):
	x = item.get('x')
	y = item.get('y')
	w = item.get('w')
	h = item.get('h')
	outer = item["outer"]
	for a in range(0, h):
		for b in range(0, w):
			map[x + b, y + a] = outer

def build_circle(map, item):
	x = item.get('x')
	y = item.get('y')
	r = item["r"] # circle radius
	t = item.get('t') # circle thickness
	if t is None:
		t = 1
	t = min(t, r)
	outer = item["outer"]
	for d in range(0, t):
		for a in range(0, 720):
			rx = int(math.sin(a/2) * (r - d)) + x
			ry = int(math.cos(a/2) * (r - d)) + y
			map[rx, ry] = outer

def build_square(map, item):
	x = item.get('x')
	y = item.get('y')
	w = item.get('w')
	h = item.get('h')
	outer = item.get('outer')
	inner = item.get('inner')

	map[x:x + w, y:y + h] = outer
	if inner is not None:
		map[x + 1:x + w - 1, y + 1:y + h - 1] = inner
