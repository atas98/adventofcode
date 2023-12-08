import operator
from collections import namedtuple
from functools import reduce
from math import ceil, sqrt
from typing import Iterable, List


Record = namedtuple('record', 'time distance')


def parse_input(input_lines: List[str]) -> Iterable[Record]:
    def split_line(line: str):
        return (int(num) for num in line.split(':')[1].split())
    return (Record(t, d) for t, d in zip(
        split_line(input_lines[0]),
        split_line(input_lines[1]),
    ))


def parse_input_part2(input_lines: List[str]) -> Record:
    def parse_line(line: str):
        return int(''.join(num for num in line.split(':')[1].split()))
    return Record(parse_line(input_lines[0]), parse_line(input_lines[1]))


def premutations_for_record(record: Record) -> int:
    return (
        ceil((-record.time - sqrt(record.time**2 - 4*record.distance)) / -2) - 1
        - (int((-record.time + sqrt(record.time**2 - 4*record.distance)) / -2) + 1) + 1
    )


def part1(input_lines: List[str]) -> int:
    return reduce(operator.mul, (
        premutations_for_record(record)
        for record in parse_input(input_lines)
    ))


def part2(input_lines: List[str]) -> int:
    return premutations_for_record(
        parse_input_part2(input_lines)
    )
