# Day 23 https://adventofcode.com/2024/day/23

import itertools as it
from collections import defaultdict
from tqdm import tqdm

# Read the input
graph = defaultdict(set) # represent the graph as a list (set) of adjacencies
with open("day23/input.txt") as f:
	for l in f:
		l = l.strip()
		a, b = l.split("-")
		graph[a].add(b)
		graph[b].add(a)

# Find the maximal clique
nodes = list(graph.keys())

pbar = tqdm()
maximals = list()
def born_kerbosch1(r:set[str], p:set[str], x:set[str]) -> None:
	pbar.update()
	if len(p) == len(x) == 0:
		maximals.append(r)
	
	while p:
		v = next(iter(p))
		born_kerbosch1(r | {v}, p & graph[v], x & graph[v])
		p.remove(v)
		x.add(v)

# Run it
born_kerbosch1(set(), set(graph.keys()), set())
pbar.close()

# Find the maximum clique which is the largest maximal clique
max_l = float("-inf")
for m in maximals:
	l = len(m)
	if l > max_l:
		maximum = m
		max_l = l

print(",".join(sorted(maximum)))