#!/usr/bin/env python3
import sys

def main(name: str = "demo"):
	pass

if __name__ == "__main__":
	if len(sys.argv) == 2:
		name = sys.argv[1]
	else:
		name = "demo"
	main(name=name)