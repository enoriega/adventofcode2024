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
				if c != '0':
					data.append(Space(blocks=int(c)))

# Start rearranging the data
left, right = [], []
start = 0

# Use two pointers, at each end to traverse the whole thing
while data:
	# Take out the last element
	curr = data.pop()
	match curr:
		case File():
			# Try to find a place for it in an open space
			moved = False
			while data:
				front = data.popleft()
				match front:
					case File():
						left.append(front)
					case Space(b):
						if curr.blocks <= b:
							left.append(curr)
							if curr.blocks < b:
								front.blocks -= curr.blocks
								left.append(front)
								if right and isinstance(right[-1], Space):
									right[-1].blocks += curr.blocks
								else:
									right.append(Space(blocks=curr.blocks))
							else:
								right.append(Space(blocks=curr.blocks))
							moved = True
							# Else we just discard this space because it was fully occupied
							break # step out of the inner loop
						else:
							left.append(front)
			if not moved:
				# We tried but couldn't find a place for it, send it to the right
				right.append(curr)
			
			# Dump back the left stack into data to continue
			while left:
				data.appendleft(left.pop())
		case Space():
			right.append(curr)
		

	
# Merge both stacks
output = left + list(reversed(right))

# Compute the checksum:
checksum = 0
ix = 0
for file in output:
	if isinstance(file, File):
		for i in range(ix, ix+file.blocks):
			checksum += file.id_*i
	ix += file.blocks

print(checksum)


