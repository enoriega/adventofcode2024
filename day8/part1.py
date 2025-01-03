import itertools as it
from collections import defaultdict

# Read data

with open("day8/input.txt") as f:
	grid = [list(l.strip()) for l in f]

# Grid dimensions
m = len(grid)
n = len(grid[0])

# Identify the "antennae" and keep track of the groups
antennae = defaultdict(list)
for ix, row in enumerate(grid):
	for jx, c in enumerate(row):
		if c not in {'.', '#'}:
			antennae[c].append((ix, jx))

# Do all pairwise comparisons to figure out the positions of the antinodes
antinodes = set() # Memory to avoid counting double antinodes

for an in antennae.values():
	if len(an) > 1:
		for a, b in it.product(an, an):
			if a != b:	# Don't do it with itself
				# Compute the differences in positions				
				i, j = a[0]+(a[0]-b[0]), a[1]+(a[1]-b[1])
				# Check to see if candidate is within bounds
				if 0 <= i < m and 0 <= j < n:
					# This is a valid antinode
					antinodes.add((i, j))

# Print unique number of antinodes
print(f"Antinodes: {len(antinodes)}")
