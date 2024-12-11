# Day 11 https://adventofcode.com/2024/day/11
import itertools as it
from tqdm import trange
# Read the initial set of stones
with open("day11/input.txt") as f:
	initial_stones = f.read().strip().split()

def blink(stones:list[str]) -> list[str]:
	""" Do one blick and return the changes """
	new_stones = []
	for stone in stones:
		match stone:
			case "0":
				new_stones.append("1")
			case even if len(even) % 2 == 0:

				pivot = len(even)//2
				left = ''.join(it.dropwhile(lambda n: n == "0", even[:pivot]))
				if not left:
					left = "0"
				right = ''.join(it.dropwhile(lambda n: n == "0", even[pivot:]))
				if not right:
					right = "0"


				new_stones.append(left)
				new_stones.append(right)
			case odd:
				new_stones.append(str(int(odd)*2024))
	return new_stones


num_blinks = 25
for _ in trange(num_blinks):
	initial_stones = blink(initial_stones)

print(f'{len(initial_stones)}')