# Day 12 https://adventofcode.com/2024/day/12

from collections import deque
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
		if (a, b) == (1, 113):
			p = 0
		if (a, b) not in seen:
			# pseeds.update()
			region = []
			# Do a BFS and just consider the neighbors of the same type
			queue = deque([(a, b)])
			# pbfs = tqdm(desc="BFS", leave=False)
			while queue:
				# pbfs.update()
				i, j = queue.popleft()
				if (i, j) not in seen:
					region.append((i, j))
					seen.add((i, j))
					for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
						x, y = i+di, j+dj
						# Check for bounds and that we haven't visited it before
						if 0 <= x < m and 0 <= y < n:
							if grid[x][y] == grid[i][j] and (x, y) not in seen:
								# This node is part of the same region
								queue.append((x, y))
			# Add the region to the list
			regions.append(region)

# Compute the price
total_price = 0
for region in regions:
	# print([grid[i][j] for i, j in region])
	perimeter = 0
	area = 0
	for i, j in region:
		area += 1
		for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
			x, y = i+di, j+dj
			# Check for bounds and that we haven't visited it before
			if 0 <= x < m and 0 <= y < n:
				if grid[x][y] != grid[i][j]:
					perimeter += 1
			else:
				perimeter += 1
	print(f"{[grid[i][j] for i, j in region]} - A: {area} - P: {perimeter}")
	total_price += area * perimeter
print(total_price)
	# print(f"{[grid[i][j] for i, j in region]} - A: {area} - P: {perimeter}")
	

