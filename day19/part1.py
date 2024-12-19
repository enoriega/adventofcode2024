# Day 19 - https://adventofcode.com/2024/day/19

from tqdm import tqdm

# Read the input
with open("day19/input.txt") as f:
	patterns = {p.strip() for p in f.readline().split(',')}
	designs = [l.strip() for l in f if l.strip()]

mem = {}
# Use a recursive approach
def solvable(design:str) -> bool:
	""" Returns of tokenization of the design is possible """
	if design in mem:
		return mem[design]
	
	ret = False
	for pattern in patterns:
		if design == pattern:
			ret = True
			break
		elif design.startswith(pattern):
			# This may be a candidate, so solve the subproblem
			sufix = design[len(pattern):]
			if solvable(sufix):
				ret = True
				break

	mem[design] = ret
	return ret


# Solve each problem (design) and count how many are solvable
possible = 0
for design in tqdm(designs):
	if solvable(design):
		possible += 1

# Print the result
print(possible)