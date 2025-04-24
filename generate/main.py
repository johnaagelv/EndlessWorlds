#!/usr/bin/env python3
import json
import numpy as np

def main():
	with open("generate/ankt.json", "rt") as f:
		world = json.load(f)
		print(f"{world!r}")

if __name__ == "__main__":
	main()