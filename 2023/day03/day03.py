from collections import namedtuple
from functools import reduce
import operator
from typing import List, Iterable


Cell = namedtuple('Cell', 'x y')
SPACE = '.'
GEAR = '*'


def get_number_len(line: str, x_start: int) -> int:
    if x_start == len(line) - 1:
        return 0
    for x in range(x_start + 1, len(line)):
        if not line[x].isdigit():
            return x - x_start
    return len(line) - x_start


def get_number_len_left(line: str, x_start: int) -> int:
    if x_start == 0:
        return 0
    for x, char in enumerate(line[x_start - 1::-1]):
        if not char.isdigit():
            return x
    return x_start


def get_adjustent_cells(cell: Cell, length: int, bounds: Cell) -> Iterable[Cell]:
    return (
        Cell(x, y)
        for y in range(cell.y - 1, cell.y + 2)
        for x in range(cell.x - 1, cell.x + length + 1)
        if not (x in range(cell.x, cell.x + length) and y == cell.y)
            and x >= 0 and y >= 0 and x < bounds.x and y < bounds.y
    )


def get_adjustent_numbers(input_lines: List[str], current_cell: Cell, bounds: Cell) -> Iterable[int]:
    adjustent_coords = get_adjustent_cells(current_cell, 1, bounds)
    for cell in adjustent_coords:
        if input_lines[cell.y][cell.x].isdigit():
            number_len_left = get_number_len_left(input_lines[cell.y], cell.x)
            number_len_right = get_number_len(input_lines[cell.y], cell.x)

            yield int(input_lines[cell.y][cell.x - number_len_left:cell.x + number_len_right])

            # Skip next related cells in the current line
            to_skip = number_len_right - 1 \
                if cell.x + number_len_right < current_cell.x + 1 \
                else current_cell.x - cell.x + 1
            for _ in range(to_skip):
                try:
                    next(adjustent_coords)
                except StopIteration:
                    break


def is_symbol(char: str) -> bool:
    return not char.isdigit() and char != SPACE


def part1(input_lines: List[str]) -> int:
    bounds = Cell(len(input_lines[0]), len(input_lines))
    part_numbers = []
    for y, line in enumerate(input_lines):
        to_skip = 0
        for x, char in enumerate(line):
            if to_skip > 0:
                to_skip -= 1
                continue

            if char.isdigit():
                num_len = get_number_len(line, x)
                adjustent_coords = get_adjustent_cells(Cell(x, y), num_len, bounds)
                to_skip = num_len - 1
                if any(is_symbol(input_lines[cell.y][cell.x])
                       for cell in adjustent_coords):
                    part_numbers.append(int(line[x:x + num_len]))

    return sum(part_numbers)


def part2(input_lines: List[str]) -> int:
    bounds = Cell(len(input_lines[0]), len(input_lines))
    ratios = []
    for y, line in enumerate(input_lines):
        for x, char in enumerate(line):
            if char == GEAR:
                adjustent_numbers = list(get_adjustent_numbers(input_lines, Cell(x, y), bounds))
                if len(adjustent_numbers) != 2:
                    continue
                ratios.append(reduce(operator.mul, adjustent_numbers))
    return sum(ratios)