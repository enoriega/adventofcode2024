# Day 22 - https://adventofcode.com/2024/day/22

import itertools as it
from collections import deque
from tqdm import tqdm
# Read the input
with open("day22/input.txt") as f:
	secrets = [int(l) for l in f]
	
def next(num:int) -> int:
	new = num*64
	new ^= num
	new %= 16777216

	num = new
	new = num//32
	new ^= num
	new %= 16777216

	num = new
	new = num*2048
	new ^= num
	new %= 16777216

	return new

# n = 123
# for _ in trange(2000):
# 	n = next(n)
# 	# print(n)

all_prices = []
for secret in tqdm(secrets, desc="Prices"):
	prices = [secret%10]
	n = secret
	for _ in range(2000):
		n = next(n)
		digit = n%10
		prices.append(digit)
	all_prices.append(prices)
	

# print(all_prices[0])
# Compute the differences
all_differences = []
for prices in tqdm(all_prices, desc="Differences"):
	differences = []
	for a, b in zip(prices, prices[1:]):
		differences.append(b-a)
	all_differences.append(differences)

# print(all_differences[0])

# Find all windows
all_windows = []
all_window_values = []
for ix, differences in enumerate(tqdm(all_differences, desc="Windows")):
	windows = set()
	window_values = {}
	window = deque()
	for jx, d in enumerate(differences):
		window.append(d)
		if len(window) == 4:
			key = tuple(window)
			windows.add(key)
			if key not in window_values:
				window_values[key] = all_prices[ix][jx+1]
		if jx >= 3:
			window.popleft()
			
	all_windows.append(windows)
	all_window_values.append(window_values)

distinct_windows = set(it.chain.from_iterable(all_windows))
print(f"Number of distinct windows observed: {len(distinct_windows)}")

def evaluate(window) -> int:
	score = 0
	for wv in all_window_values:
		score += wv.get(window, 0)
	return score

max_score = float("-inf")
for window in distinct_windows:
	score = evaluate(window)
	if score > max_score:
		max_score = score

print(max_score)



