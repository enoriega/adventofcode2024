# Day 17 https://adventofcode.com/2024/day/17

import itertools as it
from tqdm import tqdm, trange

# Read the input
data = {}
with open("day17/input.txt") as f:
	for ix, line in enumerate(f):
		if line.strip():
			_, v = line.split(":")
			if ix == 0:
				data['A'] = int(v)
			elif ix == 1:
				data['B'] = int(v)
			elif ix == 2:
				data['C'] = int(v)
			elif ix == 4:
				data['program'] = [int(n) for n in v.split(',')]

# Our simulator function
def simulate(A:int, B:int, C:int, program:list[int]) -> str:
		""" Executes the program """

		output = []
		pix = 0	# Instruction pointer
		# Go into the execution loop
		while pix < len(program):	# This statement guards against out of bounds
			# print(A, bin(A))
			instruction = program[pix]
			operand = program[pix+1]
			match instruction:
				case 0: # adv
					A //= 2**resolve_combo(operand, A, B, C)
				case 1: # bxl
					B ^= operand
				case 2: # bst
					B = resolve_combo(operand, A, B, C) % 8
				case 3: # jnz
					if A != 0:
						pix = operand
						continue # Skip incrementing the program counter
				case 4: # bxc
					B ^= C
				case 5: # out
					output.append(str(resolve_combo(operand, A, B, C)%8))
				case 6: # bdv
					B = A // 2**resolve_combo(operand, A, B, C)
				case 7: # cdv
					C = A // 2**resolve_combo(operand, A, B, C)

			# Update the program counter
			pix += 2
		
		# Build the output
		return ",".join(output)

def resolve_combo(op:int, A:int, B:int, C:int) -> int:
	if 0 <= op <= 3:
		return op
	elif op == 4:
		return A
	elif op == 5:
		return B
	elif op == 6:
		return C
	else:
		raise Exception("Reserved value in combo operand")

# target = ",".join([str(v) for v in data['program']])
# print(target)
# Get the outputs of every individual number

# space = 8**17-8**16
# for n in trange(8):
# 	data["A"] = 392+n
# 	val = simulate(**data)
# # if val == target:
# 	print(f"{n}: {val}")


target = list(data['program'])
print(target)
solutions = [0] # Seed it with zero

while target:
	num = target.pop()
	new_candidates = set()
	while solutions:
		solution = solutions.pop()
		solution <<= 3 # Shift left three bits
		for n in range(8):	# Test all possible values for this combination
			data['A'] = solution+n
			result = simulate(**data)
			if result[0] == str(num):
				new_candidates.add(solution+n)
	solutions = list(new_candidates)

print(min(solutions))



	