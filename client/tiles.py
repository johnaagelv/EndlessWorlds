import colours

# key: [Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]]
# key: [out-of-FOV definition, in-FOV definition]
tiles = {
	32: [(32, colours.gray, colours.black),(32, colours.white, colours.black),],
	35: [(35, colours.gray, colours.black),(35, colours.white, colours.darkbrown),],
	ord("w"): [(ord("w"), colours.gray, colours.black),(ord("w"), colours.green, colours.black),],
	ord("v"): [(ord("v"), colours.gray, colours.black),(ord("v"), colours.green, colours.black),],
	76: [(76, colours.gray, colours.black),(76, colours.white, colours.black),],
	ord("+"): [(ord("+"), colours.gray, colours.black),(ord("+"), colours.white, colours.black),],
	ord("_"): [(ord("_"), colours.gray, colours.black),(ord("_"), colours.white, colours.black),],
}