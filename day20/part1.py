# Day 20 - https://adventofcode.com/2024/day/20

from collections import deque


# Dimensions of the map
n, m = 0, 0
walls = set()
# Read the input
with open("day20/input.txt") as f:
	for i, row in enumerate(f):
		n += 1
		m = len(row)
		for j, c in enumerate(row):
			match c:
				case "S":
					start = i, j
				case "E":
					end = i, j
				case "#":
					walls.add((i, j))

def print_map(path={}):
	for i in range(n):
		for j in range(m):
			if (i, j) == start:
				print("S", end='')
			elif (i, j) == end:
				print("E", end='')
			elif (i, j) in walls:
				print("#", end='')
			elif (i, j) in path:
				print("O", end='')
			else:
				print(".", end='')
		print()

# print_map()

def neighbors(i, j, dist=1):
	for di, dj in ((0, dist), (dist, 0), (0, -dist), (-dist, 0)):
		x = i + di
		y = j + dj

		if 0 <= x < m and 0 <= y < n and (x, y) not in walls:
			yield x, y

# Find the distances in the only path in the map
path = deque([start])
distances = {start:0}
seen = set()
curr = start
while curr != end:
	seen.add(curr)
	for neighbor in neighbors(*curr):
		if neighbor not in seen:
			distances[neighbor] = distances[curr]+1
			path.append(neighbor)
			curr = neighbor

# print()
# print_map(path)
print(distances[end])
# For each element in the path, see if we can jump a wall
num_cheats = 0
elems = set(path)
while path:
	curr = path.popleft()
	for candidate in neighbors(*curr, dist=2):
		if candidate in elems:
			# If the difference in distances is greater than two
			# then this is a feasible cheat
			if distances[candidate] - distances[curr] > 100:
				num_cheats += 1

print(num_cheats)
