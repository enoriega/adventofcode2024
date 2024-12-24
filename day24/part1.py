#Day 24 https://adventofcode.com/2024/day/24

from copy import deepcopy
from collections import defaultdict, deque

adjacencies = defaultdict(set)
reversed_adjacencies = defaultdict(set)
types = {}
values = {}
heads = deque()
with open("day24/input.txt") as f:
	
	# Read the initial values
	while line := f.readline():
		line = line.strip()
		if not line:
			break
		node, val = line.split(": ")
		heads.append(node)
		values[node] = val == "1"
	
	# Read the edges
	for line in f:
		line = line.strip()
		t = line.split()
		s1, s2, type_, d = t[0], t[2], t[1], t[4]
		adjacencies[s1].add(d)
		reversed_adjacencies[d].add(s1)
		adjacencies[s2].add(d)
		reversed_adjacencies[d].add(s2)
		types[d] = type_

original_reversed = deepcopy(reversed_adjacencies)
# Sort the nodes topologically and compute their values along the way
while heads:
	node = heads.popleft()

	# Remove the edges from the reversed lists
	for n in adjacencies[node]:
		reversed_adjacencies[n].remove(node)
		if not reversed_adjacencies[n]:
			heads.append(n)
			# Compute the value if we have resolved all dependencies
			a, b = original_reversed[n]
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
for node in reversed(sorted((k for k in values.keys() if k[0]=="z"), key=lambda k: int(k[1:]))):
	number <<= 1
	val = int(values[node])
	number += val

print(number)