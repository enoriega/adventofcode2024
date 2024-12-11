# Day 10 https://adventofcode.com/2024/day/10
from collections import deque
# Read the input
terrain = []
with open("day10/input.txt") as f:
	terrain = [[int(c) for c in line.strip()] for line in f]

m = len(terrain)
n = len(terrain[-1])

def get_neighbors(i, j):
	""" Returns the elegible neighbors in the grid based on the rules of the problem """
	candidates = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]

	value = terrain[i][j]
	ret = []
	for x, y in candidates:
		if 0 <= x < m and 0 <= y < n and terrain[x][y] == value+1:
			ret.append((x, y))

	return ret

# Approach the problem using a breadth-first search
def bfs(i, j) -> int:
	""" Uses BFS to count the number of times 9 is reached from i, j """
	queue = deque([(i, j)])
	times_seen = 0

	while queue:
		x, y = queue.popleft()
		if terrain[x][y] == 9:
			times_seen += 1

		for n in get_neighbors(x, y):
			queue.append(n)

	return times_seen

# Find all trailheads and run BFS on each to count the score
score = 0
for i, row in enumerate(terrain):
	for j, val in enumerate(row):
		if val == 0:
			score += bfs(i, j)

print(score)



