# Day 21 - 
import itertools as it
from collections import deque, defaultdict
from functools import lru_cache
from tqdm import tqdm

# Read the input
with open("day21/test.txt") as f:
	codes = [l.strip() for l in f]	

# Class to hold the same logic that generalizes to any keypad
class KeyPad:

	def __init__(self, keys:str, scorer=None) -> None:
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

		dists, segments = self._process()
		self._distances = dists
		self._segments = segments

		if not scorer:
			scorer = self

		# Filter the segments to keep only one, the one that has the least moves
		for srcs in self._segments.values():
			for segs in srcs.values():
				min_moves = float("inf")
				chosen = None
				while segs:
					seg = segs.pop()
					moves = scorer.count_moves(seg)
					if moves < min_moves:
						min_moves = moves
						chosen = seg
				if chosen:
					segs.append(chosen)

		for s, dsts in self._segments.items():
			for d, segs in dsts.items():
				if segs:
					self._segments[s][d] = segs[0]

		x = 0
	
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
		input = list(input)
		path = []
		for jx in range(len(input)):
			if jx == 0:
				src = 'A'
			else:
				src = input[jx-1]

			segment = self._segments[src][input[jx]]
			np = list(segment)
			np.append('A')
			path.extend(np)

		return path
	

	@lru_cache()
	def _process(self) -> dict[tuple[str, str], int]:
		""" Computes all pairs shortest paths between all keys in the pad """

		ret_dists, ret_segments = {}, {}
		m = len(self._keys)
		n = len(self._keys[0])

		for i in range(m):
			for j in range(n):
				src = self._keys[i][j]
				# Ignore the empty spot
				if src.strip():
					# Do a bfs to compute distances
					dists = {src:0}
					colors = defaultdict(lambda: "white")
					predecessors = defaultdict(list)
					# predecessors[src] = None
					queue = deque([(i, j)])

					while queue:
						ci, cj = queue.popleft()
						dst = self._keys[ci][cj]
						if colors[(ci, cj)] != "black":
							colors[(ci, cj)] = "black"

						for di, dj, direction in ((0, 1, '>'), (0, -1, '<'), (1, 0, 'v'), (-1, 0, '^')):
							ni, nj = ci+di, cj+dj
							
							if 0 <= ni < m and 0 <= nj < n and self._keys[ni][nj].strip():
								neighbor = self._keys[ni][nj]
								match colors[(ni,nj)]:
									case "white":
										queue.append((ni,nj))
										dists[neighbor] = dists[dst]+1
										colors[(ni,nj)] = "gray"
										predecessors[neighbor].append((dst, direction))
									case "gray":
										if dists[dst]+1 == dists[neighbor]:
											predecessors[neighbor].append((dst, direction))

					local_segments = {}
					for dst in [k for k in it.chain.from_iterable(self._keys) if k.strip()]:
						ret = []
						segments = deque([[x] for x in predecessors[dst]])
						while segments:
							segment = segments.popleft()
							if segment:
								preds = predecessors[segment[-1][0]]
								if preds:
									for pred in preds:
										ns = list(segment)
										ns.append(pred)
										segments.append(ns)
								else:
									ret.append([s[1] for s in reversed(segment)])
						local_segments[dst] = ret
					ret_dists[src] = dists
					ret_segments[src] = local_segments

		return ret_dists, ret_segments

	def count_moves(self, seq:str) -> int:
		""" Computes the total number of moves """
		seq = list(seq)
		seq.append('A')
		return sum(self._distances[s][d] for s, d in zip(seq, seq[1:]))

arrows = " ^A\n<v>"
dirpad = KeyPad(keys=arrows)

nums = "789\n456\n123\n 0A"
numpad = KeyPad(keys=nums, scorer=dirpad)
	

# def optimize(code, steps):
# 	ret = code
# 	for step in range(steps):
# 		if step == 0:
# 			ret = numpad.encode(ret)
# 		else:
# 			ret = dirpad.encode(ret)

# 	return len(ret)

def optimize(code, steps):
	seq = numpad.encode(code)
	seq = efficient(seq, steps-1)
	return len(seq)

mem = {}
def efficient(seq, steps):
	# for _ in range(steps):
	# 	seq = dirpad.encode(seq)
	# return seq
	key = ''.join(seq), steps
	if key in mem:
		return mem[key]
	
	if steps == 0:
		ret = seq
	else:
		# Split the sequence in blocks that end in A
		blocks = []
		block = []
		for c in seq:
			block.append(c)
			if c == 'A':
				blocks.append(block)
				block = []
		if block:
			blocks.append(block)

		# Recursive call
		ret = []
		for block in blocks:
			encoded = dirpad.encode(block)
			ret.extend(efficient(encoded, steps-1))

	mem[key] = ret
	return ret


score = 0
sequences = []
for code in tqdm(codes):
	l = optimize(code, steps=26)
	num = int(code[:-1])
	score += l*num
	sequences.append(l)


for code, sequence in zip(codes, sequences):
	print(f"{code}: {sequence}")
print(score)

	