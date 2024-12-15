# Day 14 https://adventofcode.com/2024/day/14

import re
from dataclasses import dataclass

def print_grid(robots, m, n):
	from collections import Counter
	locations = Counter(((r.p0, r.p1) for r in robots))

	for i in range(m):
		for j in range(n):
			v = locations[(j, i)]
			print(v if v else '.', end='')
		print()

# Read the data
@dataclass
class Robot:
	p0:int
	p1:int

	v0:int
	v1:int

pattern = re.compile(r"^p=(?P<p0>-?\d+),(?P<p1>-?\d+) v=(?P<v0>-?\d+),(?P<v1>-?\d+)$")

with open("day14/input.txt") as f:
	robots = []
	for line in f:
		if match := pattern.match(line):
			data = {k:int(v) for k, v in match.groupdict().items()}
			robot = Robot(**data)
			robots.append(robot)

# Grid dimensions
m = 103
n = 101

# print_grid(robots, m, n)

num_seconds = 100

scores = {
	"q0": 0,
	"q1": 0,
	"q2": 0,
	"q3": 0,
}
# Iterate the map
for r in robots:
	# Use module arithmetic
	r.p0 = (r.p0 + (num_seconds*r.v0)%n)%n
	r.p1 = (r.p1 + (num_seconds*r.v1)%m)%m

	mid_row = m//2
	mid_col = n//2

	# Figure out to which quadrant it belongs
	if r.p0 < mid_col and r.p1 < mid_row:
		scores["q0"] += 1
	elif r.p0 > mid_col and r.p1 < mid_row:
		scores["q1"] += 1
	elif r.p0 < mid_col and r.p1 > mid_row:
		scores["q2"] += 1
	elif r.p0 > mid_col and r.p1 > mid_row:
		scores["q3"] += 1

# print()
# print_grid(robots, m, n)

# Multiply the scores of each quadrant
score = 1
for s in scores.values():
	score *= s

print(score)
