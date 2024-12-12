# https://adventofcode.com/2024/day/7

from typing import NamedTuple

class Problem(NamedTuple):
	target: int
	operands: list[int]

problems = []
# Read the input
with open('day7/input.txt') as f:
	for line in f:
		target, operands = line.split(":")
		problems.append(
			Problem(
				int(target),
				[int(o) for o in operands.strip().split()]
			)
		)

# Recursive approach
def is_valid(operands:list[int], target:int) -> bool:
	# Base cases
	if target == 0:
		# Got to the solution
		ret = True
	elif target < 0:
		# Can't really achieve this, (Because we excedeed the target amount later on)
		ret = False
	else:
		# Consumed the whole array and didn't get to the result
		if not operands:
			ret = False
		else:
			# Sum
			num = operands[-1]
			reminder = target - num
			rsum = is_valid(operands[:-1], reminder)

			# Mul
			reminder = target / num
			rmul = is_valid(operands[:-1], reminder)
			
			ret = rsum or rmul

	return ret

total = 0
for problem in problems:
	if is_valid(problem.operands, problem.target):
		total += problem.target

print(total)		