# https://adventofcode.com/2024/day/1

import typer
import logging
from pathlib import Path
from tqdm import tqdm

app = typer.Typer()

def read_inputs(input_file:Path) -> tuple[list[int], list[int]]:
	""" Reads the input file and returns the left and right lists in used for the challenge """
	left, right = [], []
	
	with input_file.open() as f:
		for line in f:
			l, r = line.strip().split()
			l = int(l)
			r = int(r)
			left.append(l)
			right.append(r)

	logging.info(f"Number of elements: {len(left), len(right)}")
	return left, right

@app.command()
def part1(input_file:Path) -> None:
	""" Computes the total distance between the matching ranked pairs in the parallel lists """
	
	left, right = read_inputs(input_file)
	# Heapify the lists
	import heapq
	heapq.heapify(left)
	heapq.heapify(right)

	# Start poping the top of the heaps and computing the distances
	progress = tqdm(desc="Computing distances", unit="pairs")
	distance = 0
	while left:
		l = heapq.heappop(left)
		r = heapq.heappop(right)
		# Compute the distance between the pair
		max_ = max(l, r)
		min_ = min(l, r)
		d = max_ - min_
		# Accumulate it
		distance += d
		progress.update(1)
	progress.close()

	print(f'Total distance: {distance}')

@app.command()
def part2(input_path:Path) -> None:
	""" Computes the similarity score for part 2 """
	left, right = read_inputs(input_path)

	from collections import Counter
	right = Counter(right)

	score = 0
	for l in tqdm(left, desc="Computing similarity", unit="numbers"):
		times = right[l]
		score += l*times

	print(f"Similarity: {score}")


if __name__ == "__main__":
	app()




