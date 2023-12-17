from collections import namedtuple
from itertools import combinations, groupby, pairwise
from typing import List

GALAXY_CHAR = '#'
Point = namedtuple('Galaxy', ['x', 'y'])


def parse_input(input_lines: List[str]) -> List[Point]:
    return [
        Point(x, y)
        for y, line in enumerate(input_lines)
        for x, char in enumerate(line)
        if char == GALAXY_CHAR
    ]


def find_distances_with_exp(galaxies, exp=2):
    # Search empty rows
    empty_rows = []
    for (y, _), (y_next, _) in pairwise(
        groupby(galaxies, lambda galaxy: galaxy.y)
    ):
        distance = y_next - y
        if distance == 1:
            continue
        empty_rows.extend(row for row in range(y + 1, y_next))
    # Search empty columns
    empty_cols = []
    for (x, _), (x_next, _) in pairwise(
        groupby(sorted(galaxies, key=lambda galaxy: galaxy.x),
                lambda galaxy: galaxy.x)
    ):
        distance = x_next - x
        if distance == 1:
            continue
        empty_cols.extend(col for col in range(x + 1, x_next))

    # Update galaxies coordinates based on empty rows and columns
    galaxies = (
        Point(galaxy.x + (exp - 1) * len(tuple(_ for col in empty_cols if col < galaxy.x)),
              galaxy.y + (exp - 1) * len(tuple(_ for row in empty_rows if row < galaxy.y)))
        for galaxy in galaxies
    )

    return sum(
        abs(galaxy1.x - galaxy2.x) + abs(galaxy1.y - galaxy2.y)
        for galaxy1, galaxy2 in combinations(galaxies, 2)
    )

def part1(input_lines: List[str]) -> int:
    galaxies = parse_input(input_lines)
    return find_distances_with_exp(galaxies)


def part2(input_lines: List[str]) -> int:
    galaxies = parse_input(input_lines)
    return find_distances_with_exp(galaxies, exp=1000000)
