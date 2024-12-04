# https://adventofcode.com/2024/day/4

from pathlib import Path
import typer

app = typer.Typer()

def read_input(input_path:Path) -> list[list[str]]:
	ret = []
	with input_path.open() as f:
		for line in f:
			line = line.strip()
			if line:
				ret.append(list(line))
	return ret

def count_instances(grid:list[list[str]], i:int, j:int) -> int:
	""" Counts how many times XMAS appears anchored in this point of the grid """
	times = 0

	m = len(grid)
	n = len(grid[0])
	# Forward
	if j <= n-4:
		s = "".join([grid[i][j+x] for x in range(4)])
		if s == "XMAS":
			times += 1
	# Backward
	if j >= 3:
		s = "".join([grid[i][j-x] for x in range(4)])
		if s == "XMAS":
			times += 1
	# Up
	if i >= 3:
		s = "".join([grid[i-x][j] for x in range(4)])
		if s == "XMAS":
			times += 1
	# Down
	if i <= m-4:
		s = "".join([grid[i+x][j] for x in range(4)])
		if s == "XMAS":
			times += 1
	# Southeast
	if i <= m-4 and j <= n-4:
		s = "".join([grid[i+x][j+x] for x in range(4)])
		if s == "XMAS":
			times += 1
	# Northwest
	if i >= 3 and j >= 3:
		s = "".join([grid[i-x][j-x] for x in range(4)])
		if s == "XMAS":
			times += 1
	# Southwest
	if i <= m-4 and j >= 3:
		s = "".join([grid[i+x][j-x] for x in range(4)])
		if s == "XMAS":
			times += 1
	# Northeast
	if i >= 3 and j <= m-4:
		s = "".join([grid[i-x][j+x] for x in range(4)])
		if s == "XMAS":
			times += 1

	return times

def count_x_mas(grid:list[list[str]], i:int, j:int) -> int:
	
	m = len(grid)
	n = len(grid[0])

	if 1 <= i < m-1 and 1 <= j < n-1:
		# Diagonal 1
		diag1 =  grid[i-1][j-1] == "M" and grid[i+1][j+1] == "S" or \
			grid[i-1][j-1] == "S" and grid[i+1][j+1] == "M"
			
		# Diagonal 2
		diag2 = grid[i-1][j+1] == "M" and grid[i+1][j-1] == "S" or \
			grid[i-1][j+1] == "S" and grid[i+1][j-1] == "M"
		
		return int(diag1 and diag2)
	else:
		return 0
			

	

@app.command()
def part1(input_path:Path) -> None:
	""" Finds all instances of XMAS """
	num_instances = 0

	grid = read_input(input_path)

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if grid[i][j] == "X":
				num_instances += count_instances(grid, i, j)

	print(f"XMAS times: {num_instances}")

@app.command()
def part2(input_path:Path) -> None:
	""" Finds all X-MASes """
	num_instances = 0

	grid = read_input(input_path)

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if grid[i][j] == "A":
				num_instances += count_x_mas(grid, i, j)

	print(f"X-MAS times: {num_instances}")

if __name__ == "__main__":
	app()