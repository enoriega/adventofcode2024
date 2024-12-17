# Day 14 https://adventofcode.com/2024/day/14

import re
from tqdm import trange
from dataclasses import dataclass
from collections import Counter

def print_grid(robots, m, n) -> str:
	from collections import Counter
	locations = Counter(((r.p0, r.p1) for r in robots))
	ret = []
	for i in range(m):
		for j in range(n):
			v = locations[(j, i)]
			ret.append("*" if v else ' ')
		ret.append("\n")
	return ''.join(ret)

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

with open("renders.txt", "w") as f:
	for ix in trange(10403):
		counts = Counter() # Count the number of robots on each row
		for r in robots:
			# Use module arithmetic
			r.p0 = (r.p0 + r.v0)%n
			r.p1 = (r.p1 + r.v1)%m
			counts[(r.p1, r.p0)] += 1

		# Compute entropy

		f.write("\n")
		f.write(print_grid(robots, m, n))
		f.write(str(ix+1))



