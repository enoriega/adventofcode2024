# Day 6

import itertools as it

# Convenience to fetch the next direction
directions = iter(it.cycle(["east", "south", "west", "north"]))

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


# Play the walk
seen = set()
curr = initial_position
while 0 <= curr[0] < m and 0 <= curr[1] < n:
	seen.add(curr)

	nx = step(*curr, direction=direction)
	while not grid.get(nx, True):
		direction = next(directions)
		nx = step(*curr, direction=direction)
	curr = nx

# Print the number of unique positions observed
print(len(seen))

