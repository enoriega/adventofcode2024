# Day 9: https://adventofcode.com/2024/day/9

from dataclasses import dataclass
from collections import deque

@dataclass
class File:
	id_: int
	blocks: int

@dataclass
class Space:
	blocks: int

# Read the data and build the input
data = deque()
idx = 0
with open('day9/input.txt') as f:
	for ix, c in enumerate(f.read()):
		if c != '\n':
			if ix % 2 == 0:
				data.append(File(blocks=int(c), id_=idx))
				idx += 1
			else:
				data.append(Space(blocks=int(c)))

# Start rearranging the data
output = []
start = 0

# Use two pointers, at each end to traverse the whole thing
while data:
	curr = data.popleft()
	match curr:
		case File(i, b):
			# If this is a file, then append it to the output
			if output and output[-1].id_ == i:
				output[-1].blocks += b
			else:
				output.append(curr)
		case Space(b):
			# If we popped a space, then look at the other end
			tail = None
			# We will discard all the spaces at the tail of the queue
			while data:
				tail = data.pop()
				if isinstance(tail, File):
					break

			# If we found a file, the start rearranging
			if tail:
				# Create a new instance of a file that that fills as many spaces as possible
				file = File(blocks=min(b, tail.blocks), id_=tail.id_)
				# Append it to the output
				output.append(file)
				# If there are spaces remaining, put them back into the queue
				if tail.blocks < b:
					curr.blocks -= tail.blocks
					data.appendleft(curr)
				elif tail.blocks > b:
					tail.blocks -= b
					data.append(tail)

# Compute the checksum:
checksum = 0
ix = 0
for file in output:
	for i in range(ix, ix+file.blocks):
		checksum += file.id_*i
	ix += file.blocks

print(checksum)


