# Day 16 https://adventofcode.com/2024/day/16

import heapq
from collections import defaultdict

# Read the input
with open("day16/input.txt") as f:
	map = []
	for i, line in enumerate(f):
		row = []
		for j, c in enumerate(line.strip()):
			if c == 'E':
				goal = i, j
			elif c == 'S':
				start = i, j
			row.append(c)
		map.append(row)

# Find the shortest path using Dijkstra's algorithm
queue = [(0, (start, 'E'))]
costs = defaultdict(lambda: float("inf"))
seen = set()

while queue:
	cost, (curr, direction) = heapq.heappop(queue)

	if (curr, direction) not in seen:
		seen.add((curr, direction))
		if cost < costs[curr]:
			costs[curr] = cost
		# Figure out which are the available steps at this location
		neighbors = []
		match direction:
			case 'E':
				neighbors.append((cost+1, ((curr[0], curr[1]+1), 'E')))
				neighbors.append((cost+1001, ((curr[0]-1, curr[1]), 'N')))
				neighbors.append((cost+1001, ((curr[0]+1, curr[1]), 'S')))
			case 'W':
				neighbors.append((cost+1, ((curr[0], curr[1]-1), 'W')))
				neighbors.append((cost+1001, ((curr[0]-1, curr[1]), 'N')))
				neighbors.append((cost+1001, ((curr[0]+1, curr[1]), 'S')))
			case 'N':
				neighbors.append((cost+1, ((curr[0]-1, curr[1]), 'N')))
				neighbors.append((cost+1001, ((curr[0], curr[1]-1), 'W')))
				neighbors.append((cost+1001, ((curr[0], curr[1]+1), 'E')))
			case 'S':
				neighbors.append((cost+1, ((curr[0]+1, curr[1]), 'S')))
				neighbors.append((cost+1001, ((curr[0], curr[1]-1), 'W')))
				neighbors.append((cost+1001, ((curr[0], curr[1]+1), 'E')))

		for n in neighbors:
			i, j = n[1][0]
			if 0 <= i < len(map) and 0<= j <= len(map[1]) and map[i][j] != "#":
				heapq.heappush(queue, n)

print(costs[goal])
