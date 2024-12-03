# https://adventofcode.com/2024/day/2

import typer
from pathlib import Path

app = typer.Typer()

def read_input(input_path:Path) -> list[list[int]]:
	""" Reads the input file and returns a list of list of ints """

	with input_path.open() as f:
		ret = [[int(n) for n in l.strip().split()] for l in f]

	return ret

def eval_report(report:list[int]) -> bool:
	""" Returns whether the report is safe without changing anything """
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

	return safe

@app.command()
def part1(input_path:Path) -> None:
	""" Prints the number of safe reports in the input data """
	
	# Read the file
	reports = read_input(input_path)

	# Read the levels to see if they're safe and count them
	safe_reports = 0
	for report in reports:
		
		safe = eval_report(report)

		if safe:
			safe_reports += 1


	print(f"Safe reports: {safe_reports}")

@app.command()
def part2(input_path:Path) -> None:
	""" Uses the problem dampener to tolerate one issue """

	# Read the file
	reports = read_input(input_path)

	# Read the levels to see if they're safe and count them
	safe_reports = 0
	for report in reports:
		if eval_report(report):
			safe_reports += 1
		else:
			safe = False
			# This report has at least one error
			# Identify which element violates the report and take it out to reevaluate
			for ix, val in enumerate(report):
				if ix > 0:
					prev = report[ix-1]
					# If prev and val are equal, try removing each
					if prev == val:
						a = eval_report(report[:ix-1]+report[ix:])
						b = eval_report(report[:ix]+report[ix+1:])
						if a or b:
							safe = True
							break
					# If the difference is more than 3, try removing val
					diff = abs(val-prev)
					if not 1 <= diff <= 3:
						if eval_report(report[:ix]+report[ix+1:]):
							safe = True
							break
					# If the direction is different
					if ix == 1:
						# If this is the second element try removing val and prev
						a = eval_report(report[1:])
						b = eval_report(report[:1]+report[2:])
						if a or b:
							safe = True
							break
					else:
						# Otherwise try removing val
						if eval_report(report[:ix]+report[ix+1:]):
							safe = True
							break
			if safe:
				safe_reports += 1


	print(f"Safe reports: {safe_reports}")
	
			


if __name__ == "__main__":
	app()