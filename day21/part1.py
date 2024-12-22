# Day 21 - 
import itertools as it
from collections import deque, defaultdict

# Read the input
with open("day21/input.txt") as f:
	codes = [l.strip() for l in f]


# Class to hold the same logic that generalizes to any keypad
class KeyPad:

	def __init__(self, keys:str) -> None:
		""" Initializes the keypad to its default state """
		self._keys = []
		self._positions = {}
		for i, row in enumerate(keys.split("\n")):
			new_row = list()
			for j, key in enumerate(row):
				new_row.append(key)
				if key == "A":
					self._start = (i, j)
				self._positions[key] = (i, j)
			self._keys.append(row)
	
	def decode(self, input:str) -> str:
		""" Decodes a series of steps and
		  returns the series of keys pressed by the input """
		
		decoded = []
		curr = list(self._start)
		for c in input:
			match c:
				case '<':
					curr[1] -= 1
				case '^':
					curr[0] -= 1
				case '>':
					curr[1] += 1
				case 'v':
					curr[0] += 1
				case 'A':
					decoded.append(self._keys[curr[0]][curr[1]])

		return ''.join(decoded)

	def encode(self, input:str) -> list[str]:
		""" Generates the shortest sequence of directions to type the input in the current pad """

		m = len(self._keys)
		n = len(self._keys[0])

		curr = self._start
		encodings = []
		for target in input:
			# Do a BFS to find the shortest path from the current key to the target key
			colors = {}
			queue = deque([curr])
			predecessors = defaultdict(list)
			predecessors[curr].append((None, None))
			distances = {curr: 0}

			while queue:
				i, j = queue.popleft()
				if colors.get((i,j), "white") != "black":
					colors[(i,j)] = "black"
					for di, dj, direction in ((0, 1, '>'), (0, -1, '<'), (1, 0, 'v'), (-1, 0, '^')):
						x, y = i+di, j+dj
						if 0 <= x < m and 0 <= y < n and self._keys[x][y].strip():
							match colors.get((x, y), "white"):
								case "white":
									queue.append((x, y))
									distances[(x, y)] = distances[(i, j)]+1
									colors[(x, y)] = "gray"
									predecessors[(x, y)].append(((i, j), direction))
								case "gray":
									if distances[(i, j)]+1 == distances[(x, y)]:
										predecessors[(x, y)].append(((i, j), direction))
							
			def dfs(node):				
				ret = []
				for pred, direction in predecessors[node]:
					if direction:
						sub = dfs(pred)
						if sub:
							for x in dfs(pred):
								x.append(direction)
								ret.append(x)
						else:
							ret.append([direction])

				return ret

			segments = dfs(self._positions[target])

			# If there are no segments, we are at the same location we are looking for. Punch the key
			if not segments:
				segments = [['A']]
			else:
				for s in segments:
					s.append('A')

			encodings.append(segments)

			curr = self._positions[target]
		
		# Do the product of all the segments
		ret = []
		for encoding in it.product(*encodings):
			ret.append(''.join(it.chain.from_iterable(encoding)))
		return ret
			
nums = "789\n456\n123\n 0A"
numpad = KeyPad(keys=nums)

arrows = " ^A\n<v>"
dirpad = KeyPad(keys=arrows)

def encode(sequence:str, layers:int) -> str:
	candidates = []
	for ix in range(layers):
		if ix == 0:
			candidates = numpad.encode(sequence)
		else:
			new_candidates = []
			min_l = float("inf")
			while candidates:
				candidate = candidates.pop()
				for seq in dirpad.encode(candidate):
					if len(seq) <= min_l:
						new_candidates.append(seq)
						min_l = len(seq)
			candidates = new_candidates
	best = None
	for c in candidates:
		if not best:
			best = c
		else:
			if len(c) < len(best):
				best = c
	return best

score = 0
for code in codes:
	sequence = encode(code, 3)
	print(f"{code}: {sequence}, {len(sequence)}")
	num = int(code[:-1])
	score += len(sequence)*num
print(score)