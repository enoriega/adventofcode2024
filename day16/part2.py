# Day 16 https://adventofcode.com/2024/day/16

import heapq
from collections import defaultdict, deque

# Read the input
with open("day16/input.txt") as f:
	map = []
	for i, line in enumerate(f):
		row = []
		for j, c in enumerate(line.strip()):
			if c == 'E':
				goal = i, j
			elif c == 'S':
				start = i, j, 'E'
			row.append(c)
		map.append(row)

# Find the shortest path using Dijkstra's algorithm
queue = [(0, start)]
costs = defaultdict(lambda: float("inf"))
costs[start] = 0
predecessors = defaultdict(set)
seen = set()

while queue:
	cost, curr = heapq.heappop(queue)
	direction = curr[2]

	if curr not in seen:
		seen.add(curr)
		
		# Figure out which are the available steps at this location
		neighbors = []
		match direction:
			case 'E':
				neighbors.append((cost+1, ((curr[0], curr[1]+1, 'E'))))
				neighbors.append((cost+1001, ((curr[0]-1, curr[1], 'N'))))
				neighbors.append((cost+1001, ((curr[0]+1, curr[1], 'S'))))
			case 'W':
				neighbors.append((cost+1, ((curr[0], curr[1]-1, 'W'))))
				neighbors.append((cost+1001, ((curr[0]-1, curr[1], 'N'))))
				neighbors.append((cost+1001, ((curr[0]+1, curr[1], 'S'))))
			case 'N':
				neighbors.append((cost+1, ((curr[0]-1, curr[1], 'N'))))
				neighbors.append((cost+1001, ((curr[0], curr[1]-1, 'W'))))
				neighbors.append((cost+1001, ((curr[0], curr[1]+1, 'E'))))
			case 'S':
				neighbors.append((cost+1, ((curr[0]+1, curr[1], 'S'))))
				neighbors.append((cost+1001, ((curr[0], curr[1]-1, 'W'))))
				neighbors.append((cost+1001, ((curr[0], curr[1]+1, 'E'))))

		for n in neighbors:
			i, j, _ = n[1]
			if 0 <= i < len(map) and 0<= j <= len(map[1]) and map[i][j] != "#":
				if n[0] <= costs[n[1]]:
					costs[n[1]] = n[0]
					predecessors[n[1]].add(curr)
				heapq.heappush(queue, n)

# Find the target locations with the minimum cost
min_cost = float("inf")
targets = set()
for k, v in costs.items():
	if k[:2] == goal and v <= min_cost:
		min_cost = v
		targets.add(k)

# reconstruct the paths and get the number of spots
spots = 0
seen = set() # Avoid double counting
for t in targets:
	stack = deque([t])
	while stack:
		curr = stack.popleft()
		if curr[:2] not in seen:
			spots += 1
			seen.add(curr[:2])
		stack.extend(predecessors[curr])

print(targets, min_cost, spots)
