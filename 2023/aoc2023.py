import importlib
import os
import time
from io import FileIO

import click


def _get_input_lines(input_file: FileIO) -> list[str]:
    return [line.strip() for line in input_file.readlines()]


def _format_day_result(day: int, part: int, func, input_lines: list[str]) -> None:
    """ Format and print the result of AOC day challenge with time taken
    """
    start_time = time.time()
    result = func(input_lines)
    end_time = time.time()
    click.echo(f"Day {day} Part {part}: {result} ({end_time - start_time:.4f}s)")


@click.group()
def cli():
    """Advent of Code 2023"""
    pass


@cli.command()
@click.option("--part", "-p", type=click.Choice(["1", "2", "both"]), default="both", help="Part to run")
@click.option("--input", "-i", 'input_file', type=click.File("r"), help="Input file")
@click.argument("day", type=click.INT)
def run(day, part, input_file):
    """Run a day's code"""

    # default to input.txt if no input file is specified
    if not input_file:
        input_file = open(f"day{day:02d}/input.txt")

    day = int(day)
    module = importlib.import_module(f'day{day:02d}', '.')
    input_lines = _get_input_lines(input_file)

    if part in ('1', 'both') and hasattr(module, 'part1'):
        _format_day_result(day, 1, module.part1, input_lines)
    if part in ('2', 'both') and hasattr(module, 'part2'):
        _format_day_result(day, 2, module.part2, input_lines)


@cli.command()
def runall():
    """Run all days"""
    for day in range(1, 26):
        try:
            module = importlib.import_module(f"aoc2023.day{day:02d}")
        except ModuleNotFoundError:
            continue
        input_lines = _get_input_lines(open(f"day{day:02d}/input.txt"))

        _format_day_result(day, 1, module.part1, input_lines)
        _format_day_result(day, 2, module.part2, input_lines)


if __name__ == "__main__":
    if '2023' not in os.getcwd():
        os.chdir('./2023')
    cli()