import re
import typer
from pathlib import Path

app = typer.Typer()

def read_input(input_path:Path) -> str:
	with input_path.open() as f:
		data = f.read()

	return data

pattern = re.compile(r"mul\((?P<left>\d+),(?P<right>\d+)\)")

@app.command()
def part1(input_path:Path) -> None:
	data = read_input(input_path)

	# Use regex (is that cheating?)
	matches = pattern.findall(data)

	total = 0
	# Execute them
	for match in matches:
		total += int(match[0]) * int(match[1])

	print(f"Total product: {total}")


pattern2 = re.compile(r"(?P<mul>mul\((?P<left>\d+),(?P<right>\d+)\))|(?P<do>do\(\))|(?P<dont>don't\(\))")
@app.command()
def part2(input_path:Path) -> None:
	data = read_input(input_path)

	# Use regex (is that cheating?)
	matches = pattern2.findall(data)

	total = 0
	enabled = True
	# Execute them
	for match in matches:
		# Mini state machine
		if match[3] == "do()":
			enabled = True
		elif match[4] == "don't()":
			enabled = False
		else:
			if enabled:
				total += int(match[1]) * int(match[2])

	print(f"Total product: {total}")

if __name__ == "__main__":
	app()
