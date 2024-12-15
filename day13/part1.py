# Day 13 https://adventofcode.com/2024/day/13

import re
import itertools as it
from typing import NamedTuple, Optional
from tqdm import tqdm


class Problem(NamedTuple):
	""" Represents an instance of a problem """
	a:tuple[int, int]
	b:tuple[int, int]
	prize:tuple[int, int]

# Extractor helper
pattern = re.compile(r"X[\+=](\d+), Y[\+=](\d+)")
# Read the input
with open("day13/input.txt") as f:
	problems = []
	# Group the inputs in batches of 4 lines
	for batch in it.batched(f, 4):
		data = {}
		keys = ["a", "b", "prize"]
		for ix, line in enumerate(batch):
			match = pattern.search(line)
			if match:
				x = int(match.group(1))
				y = int(match.group(2))
				data[keys[ix]] = (x, y)
		problems.append(Problem(**data))

# Token costs
COST_A = 3
COST_B = 1

mem = {}
# Use a recursive approach
def solve(position:tuple[int, int], p:Problem, remaining_a:int, remaining_b:int) -> Optional[int]:
	key = (position, p, remaining_a, remaining_b)

	if key in mem:
		return mem[key]

	# Base cases
	if position == p.prize:
		ret = 0
	elif remaining_a == remaining_b == 0:
		ret = None
	# Recursive steps
	else:
		# Option 1: Press A
		if remaining_a > 0:
			pos_a = position[0]+p.a[0], position[1]+p.a[1]
			a = solve(pos_a, p, remaining_a-1, remaining_b)
			if a is None:
				a = float("inf")
		else:
			a = float("inf")

		# Option 2: Press B
		if remaining_b > 0:
			pos_b = position[0]+p.b[0], position[1]+p.b[1]
			b = solve(pos_b, p, remaining_a, remaining_b-1)
			if b is None:
				b = float("inf")
		else:
			b = float("inf")

		# No solution
		if a == b == float("inf"):
			ret = None
		# Minimize solution
		else:
			ret = min(COST_A+a, COST_B+b)
		

	mem[key] = ret
	return ret

max_steps = 100
# Aggregate solutions
total_tokens = 0
for problem in tqdm(problems):
	solution = solve((0, 0), problem, max_steps, max_steps)
	if solution:
		total_tokens += solution

print(total_tokens)