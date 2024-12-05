import itertools as it
from collections import defaultdict, deque

from typing import Optional

def main():
	# Read the data
	with open("day5/input.txt") as f:
		# Read rules
		rules = [[int(n) for n in l.split('|')] for l in it.takewhile(lambda line: line.strip(), f)]
		# Read the updates
		updates = [[int(n) for n in l.split(',')] for l in f]

	# Build lists of predecessors
	predecessors = defaultdict(set)

	for h, t in rules:
		# Add the predecessor to the corresponding list
		predecessors[t].add(h)

	
	def validate_update(update:list[int]) -> bool:
		""" Check if any element to the right doesn't occur to the left """
		successors = set()
		for current in reversed(update):
			if len(predecessors[current] - successors) < len(predecessors[current]):
				return False
			successors.add(current)
		return True



	# Now check the updates to see if they are valid
	total = 0 # Accumulate the middle elements here
	for update in updates:
		is_valid = validate_update(update)
		if is_valid:
			total += update[len(update)//2]

	print(total)




		


if __name__ == "__main__":
	main()

