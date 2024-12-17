# Day 15 https://adventofcode.com/2024/day/15
import itertools as it
from collections import deque

# Read the input
with open("day15/input.txt") as f:
	grid = []
	steps = deque()

	# Read the grid
	while line := f.readline():
		line = line.strip()
		if line:
			grid.append(list(line)) # Make it a list to make it mutable
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
	
	# Start collecting elements to move
	stack = []
	# Accumulate the elements until hitting a wall or an empty cell
	while grid[loc[0]][loc[1]] not in {'.', '#'}:
		stack.append(grid[loc[0]][loc[1]])
		match step:
			case '<':
				loc[1] -= 1
			case '>':
				loc[1] += 1
			case '^':
				loc[0] -= 1
			case 'v':
				loc[0] += 1
	
	scooch = grid[loc[0]][loc[1]] == "."
	# Unwind the steps and the appropriate step
	while stack:
		elem = stack.pop()
		if scooch:
			# Move everything on the direction
			grid[loc[0]][loc[1]] = elem
		# Otherwise we do nothing, because we hit a wall

		# Revert the step
		match step:
			case '<':
				loc[1] += 1
			case '>':
				loc[1] -= 1
			case '^':
				loc[0] += 1
			case 'v':
				loc[0] -= 1
	# Put an emty space at the begining if scooching
	if scooch:
		grid[loc[0]][loc[1]] = '.'
		match step:
			case '<':
				loc[1] -= 1
			case '>':
				loc[1] += 1
			case '^':
				loc[0] -= 1
			case 'v':
				loc[0] += 1
		robot = loc

	
print_grid(grid)
print(robot)
score = 0

for i, row in enumerate(grid):
	for j, c in enumerate(row):
		if c == "O":
			score += (100*i)+j
print(score)