import operator
from functools import reduce
from typing import Iterable, List

COLORS = ('red', 'green', 'blue')


def parse_line(line: str) -> Iterable[dict[str, int]]:
    return (
        dict(record.split(' ')[::-1] for record in subset.split(', '))
        for subset in line.split(': ')[1].split('; ')
    )


def part1(input_lines: List[str]) -> int:
    LIMITS = {'red': 12, 'green': 13, 'blue': 14}
    return sum(
        i for i, line in enumerate(input_lines, 1)
        if not any(
            any(
                int(number) > LIMITS[color]
                for color, number in record.items()
            )
            for record in parse_line(line)
        )
    )


def part2(input_lines: List[str]) -> int:
    def invert_records(game_records: Iterable[dict[str, int]]) -> dict[str, Iterable[int]]:
        return {
            color: [int(record[color]) for record in game_records if color in record]
            for color in COLORS
        }

    def get_max_records(game_records: dict[str, Iterable[int]]) -> Iterable[int]:
        return (max(records) for records in game_records.values() if records)

    return sum(reduce(
        operator.mul,
        get_max_records(invert_records(list(parse_line(line)))),
    ) for line in input_lines)
