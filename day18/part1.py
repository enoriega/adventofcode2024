# Day 18 https://adventofcode.com/2024/day/18
import heapq
from collections import defaultdict

n = 71
# Read the input
with open("day18/input.txt") as f:
	memory = [list(map(int, l.split(","))) for l in f]

# Use a sparce representaiton of the memory space
space = defaultdict(lambda: True)
for i, j in memory[:1024]:		# Only consider the first 1KB bytes
	space[j, i] = False	# Mark the memory blocks fallen down as False

# Use dijkstra to find the shortest path from the top left to the bottom right
distances = defaultdict(lambda: float("inf"))
parents = defaultdict()
queue = [(0, (0, 0, None))]
seen = set()


while queue:
	dist, (x, y, parent) = heapq.heappop(queue)	# Pop the closest node

	if (x, y) not in seen:
		seen.add((x, y))
		if dist < distances[x, y]:
			parents[x, y] = parent
			distances[x, y] = dist
		# Look at the neighbors
		for dx, dy in [(0,1), (0, -1), (1, 0), (-1,0)]:
			i = x+dx
			j = y+dy

			if 0 <= i < n and 0 <= j < n and space[i, j]:	# Check that the candidate neighbor is not corrupted
				heapq.heappush(queue, (dist+1, (i, j, (x, y))))

route = set()
curr = (n-1, n-1)
while curr:
	route.add(curr)
	curr = parents[curr]
	
for i in range(n):
	row = []
	for j in range(n):
		if (i, j) in route:
			c = "O"
		elif space[i, j]:
			c = "."
		else:
			c = "#"
		
		row.append(c)
	print(''.join(row))

print(distances[n-1, n-1])


