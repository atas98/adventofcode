from itertools import pairwise
from typing import Iterable, List


def parse_input(input_lines: List[str]) -> Iterable[List[int]]:
    return ([int(n) for n in line.split()] for line in input_lines)


def get_next_value(numbers: List[int]) -> int:
    def get_diffs(numbers: Iterable[int]) -> Iterable[int]:
        return list(b - a for a, b in pairwise(numbers))

    diffs = [numbers]
    while any(diffs[-1]):
        diffs.append(get_diffs(diffs[-1]))

    return sum(diff[-1] for diff in diffs)


def part1(input_lines: List[str]) -> int:
    return sum(map(get_next_value, parse_input(input_lines)))


def part2(input_lines: List[str]) -> int:
    return sum(
        get_next_value(list(reversed(line)))
        for line in parse_input(input_lines)
    )
