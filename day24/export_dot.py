from collections import defaultdict


types = {}
labels = {}
edges = []

with open("day24/input.txt") as f:
	
	# Read the initial values
	while line := f.readline():
		line = line.strip()
		if not line:
			break
		node, val = line.split(": ")
		labels[node] = f"{node}"
		types[node] = "circle"
	
	# Read the edges
	for line in f:
		line = line.strip()
		t = line.split()
		s1, s2, type_, d = t[0], t[2], t[1], t[4]
		labels[d] = f"{type_}\n{d}"
		types[d] = "box"
		edges.append((s1, d))
		edges.append((s2, d))

print("graph graphname {")
for node in labels:
	label = labels[node]
	style = types[node]
	print(f'{node} [label="{label}";shape={style}]')
for a, b in edges:
	print(f"{a} -- {b}")
print("}")
