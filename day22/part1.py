# Day 22 - https://adventofcode.com/2024/day/22

from tqdm import trange, tqdm
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

score = 0
for secret in tqdm(secrets):
	n = secret
	for _ in range(2000):
		n = next(n)
	score += n
	# print(f"{secret}: {n}")

print(score)


