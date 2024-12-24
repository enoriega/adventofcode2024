# Day 23 https://adventofcode.com/2024/day/23

import itertools as it
from collections import defaultdict
from tqdm import tqdm

# Read the input
graph = defaultdict(set) # represent the graph as a list (set) of incidences
with open("day23/input.txt") as f:
	for l in f:
		l = l.strip()
		a, b = l.split("-")
		graph[a].add(b)
		graph[b].add(a)

# Find all the cliques of size 3
clique_size = 3
candidates_sets = {frozenset(c) for c in it.product(*it.repeat(graph.keys(), times=clique_size))}
candidates_sets = set(filter(lambda c: len(c) == clique_size, candidates_sets))

def is_clique(candidates):
	members = list(candidates)
	hit = True
	for ix, n in enumerate(members):
		for jx in range(len(members)):
			if ix != jx:
				if n not in graph[members[jx]]:
					hit = False
					break
		if not hit:
			break
	return hit

cliques = set()
for candidates in tqdm(candidates_sets):
	if is_clique(candidates):
		# Only keep those with a member that starts with "t"
		record = False
		for member in candidates:
			if member[0] == "t":
				record = True
				break
		if record:
			cliques.add(candidates)


print(len(cliques))
