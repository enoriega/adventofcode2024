# Day 12 https://adventofcode.com/2024/day/12

import itertools as it
from collections import deque, defaultdict
from tqdm import tqdm

# Read the grid:
with open("day12/input.txt") as f:
	grid = [list(line.strip()) for line in f.readlines()]

m = len(grid)
n = len(grid[0])



# Follow a BFS-based approach
regions = [] # Store the regions here

# Store the "seeds"
seen = set()

# pseeds = tqdm(desc="Seeds")
# Iterate over the seed nodes
for a in range(m):
	for b in range(n):
		if (a, b) not in seen:
			# pseeds.update()
			region = set()
			# Do a BFS and just consider the neighbors of the same type
			queue = deque([(a, b)])
			# pbfs = tqdm(desc="BFS", leave=False)
			while queue:
				# pbfs.update()
				i, j = queue.popleft()
				if (i, j) not in seen:
					region.add((i, j))
					seen.add((i, j))
					for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
						x, y = i+di, j+dj
						# Check for bounds and that we haven't visited it before
						if 0 <= x < m and 0 <= y < n:
							if grid[x][y] == grid[i][j] and (x, y):
								# This node is part of the same region
								queue.append((x, y))
			# Add the region to the list
			regions.append(region)

def count_corners(region:set[tuple[int, int]]) -> dict[tuple[int, int], str]:
	ret = 0

	for i, j in region:
		top = i - 1, j
		bottom = i + 1, j
		left = i, j - 1
		right = i, j + 1

		if top not in region and left not in region:
			ret += 1
		if top not in region and right not in region:
			ret += 1
		if bottom not in region and left not in region:
			ret += 1
		if bottom not in region and right not in region:
			ret += 1

		if bottom in region and right in region and (bottom[0], bottom[1]+1) not in region:
			ret += 1
		if bottom in region and left in region and (bottom[0], bottom[1]-1) not in region:
			ret += 1
		if top in region and right in region and (top[0], top[1]+1) not in region:
			ret += 1
		if top in region and left in region and (top[0], top[1]-1) not in region:
			ret += 1

	return ret

# Compute the price
total_price = 0
for region in regions:
	area = len(region)

	# The number or sides if the number of corners
	sides = count_corners(region)

	# print(f"{[grid[i][j] for i, j in region]} - A: {area} - S: {sides}")
	total_price += area * sides
print(total_price)
	

