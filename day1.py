# https://adventofcode.com/2024/day/1

import typer
import heapq
from pathlib import Path
from tqdm import tqdm

def main(input_file:Path):
	left, right = [], []
	
	with input_file.open() as f:
		for line in f:
			l, r = line.strip().split()
			l = int(l)
			r = int(r)
			left.append(l)
			right.append(r)

	print(f"Number of elements: {len(left), len(right)}")

	# Heapify the lists
	heapq.heapify(left)
	heapq.heapify(right)

	# Start poping the top of the heaps and computing the distances
	progress = tqdm(desc="Computing distances", unit="pairs")
	distance = 0
	while left:
		l = heapq.heappop(left)
		r = heapq.heappop(right)
		max_ = max(l, r)
		min_ = min(l, r)
		d = max_ - min_
		distance += d
		progress.update(1)
	progress.close()

	print(f'Total distance: {distance}')


if __name__ == "__main__":
	typer.run(main)




