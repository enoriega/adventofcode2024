# Day 6

import itertools as it
from copy import deepcopy
from tqdm import tqdm

# Convenience to fetch the next direction
directions = {"north":"east", "east":"south", "south":"west", "west":"north"}

# Read the data
with open("day6/input.txt") as f:
	data = f.readlines()


# Create grid - True is available, False if blocked
grid  = {}
m = n = 0
for i, line in enumerate(data):
	m += 1
	for j, c in enumerate(line.strip()):
		n += 1
		grid[i, j] = c == '.'
		if c == "^":
			grid[i, j] = True
			initial_position = (i, j)
			direction = "north"


def step(i, j, direction):
	""" Gets the next cell according to the rules """
	match direction:
		case "north":
			return i-1, j
		case "south":
			return i+1, j
		case "east":
			return i, j+1
		case "west":
			return i, j-1

visited = set()

def walk(grid, curr, direction) -> bool:
	# Play the walk
	seen = set()
	blocked = set()
	while 0 <= curr[0] < m and 0 <= curr[1] < n:
		visited.add(curr)
		if (curr, direction) in seen:
			return False

		seen.add((curr, direction))		

		# Normal step
		nx = step(*curr, direction=direction)
		while not grid.get(nx, True):
			direction = directions[direction]
			nx = step(*curr, direction=direction)


		curr = nx

	if blocked:
		print(len(blocked))

	return True

walk(grid, initial_position, direction)
blocks = 0

for i, j in tqdm(set(visited)):
		if (i, j) != initial_position:
			new_grid = deepcopy(grid)
			new_grid[i,j] = False
			if not walk(new_grid, initial_position, direction):
				blocks += 1

print(blocks)
