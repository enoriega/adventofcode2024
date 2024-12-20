# Day 20 - https://adventofcode.com/2024/day/20

from collections import deque, Counter

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

# Find all cells in the path within a manhattan distance of 20
num_cheats = 0
elems = set(path)
while path:
	curr = path.popleft()
	elems.remove(curr)
	candidates = []
	for i in range(-20, 21):
		for j in range(-20, 21):
			if (i, j) != (0, 0):
				candidates.append((curr[0]+i, curr[1]+j))

	# Verify if there is a fesible cheat
	for candidate in candidates:
		# Only consider the candidate if it is part of the path
		if candidate in elems:
			# How far is the candidate from the current cell if were to cheat
			cheat_distance = abs(curr[0]-candidate[0]) + abs(curr[1]-candidate[1])
			# How far is the candidate if we follow the path
			normal_distance = distances[candidate] - distances[curr]
			# What is the net distance savings
			savings = normal_distance-cheat_distance
			# If there are net savings and the cheat is no more than 20 blocks away
			if cheat_distance <= 20 and savings:
				if savings >= 100:
					num_cheats += 1

print(num_cheats)
