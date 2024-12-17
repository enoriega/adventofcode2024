# Day 15 https://adventofcode.com/2024/day/15
import itertools as it
from collections import deque

# Read the input
with open("day15/input.txt") as f:
	grid = []
	steps = deque()

	# Read the grid
	while line := f.readline():
		if line.strip():
			row = []
			for c in line:
				match c:
					case "#":
						row += ["#", "#"]
					case ".":
						row += [".", "."]
					case "O":
						row += ["[", "]"]
					case "@":
						row += ["@", "."]
			grid.append(row) # Make it a list to make it mutable
		else:
			break

	# Read the steps
	steps = deque(it.chain.from_iterable(l.strip() for l in f.readlines()))

# Locate the robot
for i, row in enumerate(grid):
	for j, c in enumerate(row):
		if c == "@":
			robot = [i, j]

def print_grid(grid):
	for row in grid:
		print(''.join(row))
	print()

print_grid(grid)

loc = robot
# Now start the walk
while steps:
	# Fetch the next step
	step = steps.popleft()
	
	# Do BFS to identify all the cells to move
	queue = deque([(loc, "@")])
	move = True
	to_move = []
	seen = set()
	while queue:
		curr, symbol = queue.popleft()
		if tuple(curr) not in seen:
			to_move.append((curr, symbol))
			seen.add(tuple(curr))

			neighbors = []
			# Depending on the direction
			match symbol, step:
				# If stepping to the sides
				case _, '<' | '>' as s:
					n = list(curr)
					n[1] -= 1 if s == '<' else -1 # Adjust the next location based on the direction of the step
					neighbors.append(n)
					
				# If stepping vectically
				case _, '^' | 'v' as s:
					nx = list(curr)
					nx[0] -= 1 if s == "^" else -1
					neighbors.append(nx)

					left = curr[0], curr[1]-1
					right = curr[0], curr[1]+1
					
					# If the current node is a block, bring its other side along
					if symbol == "]" and grid[left[0]][left[1]] == "[":
						neighbors.append(left)
					elif symbol == "[" and grid[right[0]][right[1]] == "]":
						neighbors.append(right)

			# Add the neighbors to the queue
			for n in neighbors:
				match grid[n[0]][n[1]]:
					case "#":
						# We stumbled upon a wall, abort the movement
						move = False
						break
					case s if s != ".":
						queue.append((n, s))
	
	# If we are cleared to move, start popping the chosen elements and moving them
	if move:
		while to_move:
			(i, j), s = to_move.pop()
			match step:
				case '<':
					loc = [i, j-1]
				case '>':
					loc = [i, j+1]
				case '^':
					loc = [i-1, j]
				case 'v':
					loc = [i+1, j]
			grid[loc[0]][loc[1]] = s
			grid[i][j] = '.'
	# print(step)
	# print_grid(grid)
							
	

	
print_grid(grid)
print(robot)
score = 0

for i, row in enumerate(grid):
	for j, c in enumerate(row):
		if c == "[":
			score += (100*i)+j
print(score)