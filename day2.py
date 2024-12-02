# https://adventofcode.com/2024/day/2

import typer
from pathlib import Path

app = typer.Typer()

def read_input(input_path:Path) -> list[list[int]]:
	""" Reads the input file and returns a list of list of ints """

	with input_path.open() as f:
		ret = [[int(n) for n in l.strip().split()] for l in f]

	return ret

@app.command()
def part1(input_path:Path) -> None:
	""" Prints the number of safe reports in the input data """
	
	# Read the file
	reports = read_input(input_path)

	# Read the levels to see if they're safe and count them
	safe_reports = 0
	for report in reports:
		safe = True
		
		# Iterate through the levels to make sure it is monotonic and the difference is within bounds
		for ix in range(1, len(report)):
			# First iteration, set the increasing flag appropriately
			if report[ix] > report[ix-1]:
				if ix == 1:
					increasing = True
				elif not increasing:
					safe = False
						
			elif report[ix] < report[ix-1]:
				if ix == 1:
					increasing = False
				elif increasing:
					safe = False
			else:
				safe = False

			if not(1 <= abs(report[ix] - report[ix-1]) <= 3):
				safe = False
			
			if not safe:
				break

		if safe:
			safe_reports += 1


	print(f"Safe reports: {safe_reports}")


if __name__ == "__main__":
	app()