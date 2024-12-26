#Day 24 https://adventofcode.com/2024/day/24

import itertools as it
from copy import deepcopy
from collections import defaultdict, deque
from tqdm import trange
from functools import lru_cache

adjacencies = defaultdict(set)

types = {}
values = {}
heads = []
nodes = set()
reversed_adjacencies = defaultdict(set)

with open("day24/input.txt") as f:
	
	# Read the initial values
	while line := f.readline():
		line = line.strip()
		if not line:
			break
		node, val = line.split(": ")
		heads.append(node)
		values[node] = val == "1"
	
	max_z = float("-inf")
	max_x = float("-inf")
	# Read the edges
	for line in f:
		line = line.strip()
		t = line.split()
		s1, s2, type_, d = t[0], t[2], t[1], t[4]
		adjacencies[s1].add(d)
		adjacencies[s2].add(d)
		reversed_adjacencies[d].add(s1)
		reversed_adjacencies[d].add(s2)
		types[d] = type_
		nodes.add(s1)
		nodes.add(s2)
		nodes.add(d)

		for n in (s1, s2, d):
			if n[0] == "z":
				num = int(n[1:])
				if num > max_z:
					max_z = num
			if n[0] == "x":
				num = int(n[1:])
				if num > max_x:
					max_x = num
num_digits = 2
target_nodes = list(reversed([f"z{str(i).zfill(num_digits)}" for i in range(max_z+1)]))

num_nodes = len(nodes)
num_pairs = (num_nodes**2-num_nodes)//2
num_combinations = (num_pairs**2-num_pairs)//2
num_combinations = (num_combinations**2-num_combinations)//2
print(f"Num nodes: {num_nodes}")
print(f"Num pairs: {num_pairs}")
# print(f"Possible 4-swaps: {num_combinations}")

# Compute the target value
num_bits = 0
target_value = 0
for num in reversed(range(max_x+1)):
	num_bits += 1
	target_value <<= 1
	target_value += values[f"x{str(num).zfill(num_digits)}"]
	target_value += values[f"y{str(num).zfill(num_digits)}"]

# target_value = x+y
print(f"Target value: {target_value}")

def run_circuit():
	hs = deque(heads)
	working_reversed = deepcopy(reversed_adjacencies)
	# working_values = deepcopy(values)
	
	# Sort the nodes topologically and compute their values along the way
	while hs:
		node = hs.popleft()
		# Remove the edges from the reversed lists
		for n in adjacencies[node]:
			working_reversed[n].remove(node)
			if not working_reversed[n]:
				hs.append(n)
				# Compute the value if we have resolved all dependencies
				a, b = reversed_adjacencies[n]
				va = values[a]
				vb = values[b]
				match types[n]:
					case "XOR":
						val = va ^ vb
					case "OR":
						val = va | vb
					case "AND":
						val = va & vb
				values[n] = val

	# Get the z values
	number = 0
	for node in target_nodes:
		number <<= 1
		val = int(values[node])
		number += val

	return number

def swap(a, b):
	
	parents_a = reversed_adjacencies[a]
	parents_b = reversed_adjacencies[b]

	reversed_adjacencies[a] = parents_b
	reversed_adjacencies[b] = parents_a
	for pa in parents_a:
		adjacencies[pa].remove(a)
		adjacencies[pa].add(b)

	for pb in parents_b:
		adjacencies[pb].remove(b)
		adjacencies[pb].add(a)

	children_a = adjacencies[a]
	children_b = adjacencies[b]

	adjacencies[a] = children_b
	adjacencies[b] = children_a

	for ca in children_a:
		reversed_adjacencies[ca].remove(a)
		reversed_adjacencies[ca].add(b)

	for cb in children_b:
		reversed_adjacencies[cb].remove(b)
		reversed_adjacencies[cb].add(a)

@lru_cache()
def get_dependencies(node):
	seen = set()
	queue = deque([node])

	while queue:
		curr = queue.popleft()
		if curr not in seen:
			seen.add(curr)
			for n in reversed_adjacencies[curr]:
				queue.append(n)

	return seen - {node}

@lru_cache()
def get_successors(node):
	seen = set()
	queue = deque([node])

	while queue:
		curr = queue.popleft()
		if curr not in seen:
			seen.add(curr)
			for n in adjacencies[curr]:
				queue.append(n)

	return seen - {node}

def find_swap_candidates(node, exclude=None):
	dependencies = get_dependencies(node)
	if not exclude:
		exclude = set()
		
	candidates = dependencies - exclude

	target_val = not values[node]
	op = types[node]

	ret = []
	for c in candidates:
		if c[0] not in {"x", "y", "z"}:
			a, b = reversed_adjacencies[c]
			va, vb = values[a], values[b]
			match op:
				case "AND":
					cval = va & vb
				case "OR":
					cval = va | vb
				case "XOR":
					cval = va ^ vb
			if cval == target_val:
				ret.append(c)
	return ret

def compare_bits(target, number):
	""" Returns: num of matching bits, bit ix to change, bit target val"""
	ix = 0
	start = None
	end = None

	tn = 0
	nn = 0

	while target > 0:
		t = target % 2
		n = number % 2

		if start is None and t != n:
			start = ix
		elif start is not None and end is None and  t == n:
			end = ix-1

		if start is not None and end is None:
			t <<= (ix-start)
			n <<= (ix-start)
			tn += t
			nn += n

		target >>= 1
		number >>= 1

		ix += 1
	
	if start is not None:
		num_equal = start
		diff = tn - nn
		if diff == 1:
			bit_ix = end
			target_val = True
		else:
			bit_ix = end
			target_val = False

	else:
		num_equal = ix
		bit_ix = None
		target_val = None

	return num_equal, bit_ix, target_val

current_val = run_circuit()
# print(target_value, bin(target_value))
# print(current_val, bin(current_val))
last_changed = []
def solve(current_val:int) -> list[tuple[int, int]]:
	
	ret = []
	# Identify the bit position to shift
	# current_val = run_circuit()
	_, target_ix, _ = compare_bits(target_value, current_val)
	if target_ix is not None:
		mask = 0
		for _ in range(target_ix+1):
			mask <<= 1
			mask += 1
		# Try all possible swaps at target_ix
		node = f"z{str(target_ix).zfill(num_digits)}"
		# Exclude the dependencies of the nodes that are already correct
		exclude = set()
		for ix in range(target_ix):
			exclude |= get_dependencies(f"z{str(ix).zfill(num_digits)}")
		# exclude = last_changed[-1] if last_changed else None
		last_changed.append(node)
		for target_node in get_dependencies(node):
			if target_node[0] not in {"x", "y"}:
				# Try all the swaps and find which are valid
				# candidates = find_swap_candidates(target_node, exclude)
				candidates = nodes
				for candidate in candidates:
					key = (target_node, candidate)
					
					# Change the circuit and its values
					swap(target_node, candidate)
					candidate_result = run_circuit()
					# Compare the result to see if it is a match
					if (target_value & mask) == (candidate_result & mask):
						# print()
						# print(bin(target_value))
						# print(bin(candidate_result))
						ret.append(key)
					# Undo the circuit change
					swap(target_node, candidate)
					restored_val = run_circuit()
					assert restored_val == current_val

	else:
		# No solution so return empty list with no sequence of swaps
		pass

	return ret


print(bin(target_value))
print(bin(current_val))
solve(current_val)


# 10,20,32,39
ixs = [10,20,32,40]
dependencies =[]
for ix in ixs:
	dependencies.append(get_dependencies(f"z{str(ix).zfill(num_digits)}"))

exclusive_dependencies = []
for ix, deps in enumerate(dependencies):
	ed = set()
	for jx, other in enumerate(dependencies):
		if ix != jx:
			ed |= other
	exclusive_dependencies.append(deps-ed)

# print(exclusive_dependencies)
# print(len(dependencies))
