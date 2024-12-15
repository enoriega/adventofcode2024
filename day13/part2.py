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
				if ix == 2:
					x += 10000000000000
					y += 10000000000000
				data[keys[ix]] = (x, y)
		problems.append(Problem(**data))

# Token costs
COST_A = 3
COST_B = 1


# Use a bottom up approach to find chepaest path
def solve(p:Problem) -> Optional[int]:
	# Frame the problem as a system of linear equations.
	# If a solution exists where the coefficients are both integers, then that is the exact solution

	W = [(p.a[0], p.b[0]), (p.a[1], p.b[1])]
	y = p.prize

	# We are looking for vector x
	determiner = W[0][0]*W[1][1]-W[0][1]*W[1][0]

	# Solve the system using Cramer's rule
	x0 = (y[0]*W[1][1]-y[1]*W[0][1]) // determiner
	x1 = (y[1]*W[0][0]-y[0]*W[1][0]) // determiner


	product = (W[0][0]*x0+W[0][1]*x1), (W[1][0]*x0+W[1][1]*x1)

	if product == y:
		return x0*COST_A + x1*COST_B
	else:
		return None

# Aggregate solutions
total_tokens = 0
for problem in tqdm(problems):
	solution = solve(problem)
	if solution:
		total_tokens += solution

print(total_tokens)