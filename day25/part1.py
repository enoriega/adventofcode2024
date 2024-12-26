# Day 25 - https://adventofcode.com/2024/day/25

from tqdm import tqdm
# Read the input
locks = []
keys = []
with open("day25/input.txt") as f:
	block = []
	for l in f:
		l = l.strip()
		if l:
			block.append(l)
		else:
			if block[0] == "#####":
				locks.append(block)
			else:
				keys.append(block)
			block = []
	if block:
		if block[0] == "#####":
			locks.append(block)
		else:
			keys.append(block)
		block = []

def parse(block, is_lock) -> list[int]:
	heights = [0,0,0,0,0]
	if is_lock:
		block = block[1:]
	else:
		block = block[:-1]

	for l in block:
		for ix, c in enumerate(l):
			if c == "#":
				heights[ix] += 1
	return heights

def fits(lock, key) -> bool:
	ret = True
	for l, k in zip(lock, key):
		if l + k > 5:
			ret = False
			break
	return ret

keys = [parse(k, is_lock=False) for k in keys]
locks = [parse(k, is_lock=True) for k in locks]

total_fit = 0
for lock in tqdm(locks):
	for key in keys:
		if fits(lock, key):
			total_fit += 1

print(total_fit)





# print(len(locks))
# print(len(keys))
# print(len(locks)*len(keys))