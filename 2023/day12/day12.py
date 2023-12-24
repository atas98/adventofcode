import asyncio
from collections import namedtuple
from functools import cache
from typing import Iterable, List, Tuple

Record = namedtuple("Record", ["row", "groups"])


def parse_input(input_lines: List[str]) -> Iterable[Record[str, List[int]]]:
    return (
        Record(
            row,
            tuple(int(group) for group in groups.split(",")),
        )
        for row, groups in (row.split(" ") for row in input_lines)
    )


@cache
def attempt(row: str, template: Tuple[int]) -> int:
    row = row.lstrip('.')
    if not template:
        return '#' not in row
    next_group_len = template[0]
    if not row or sum(template) > len(row) - row.count('.'):
        return 0
    if '.' not in row[0:next_group_len] and (
        len(row) == next_group_len or row[next_group_len] in ('.', '?')
    ):
        # Check if there is enough space for next group
        next_idx = next_group_len + 1 if next_group_len < len(row) else next_group_len
        return attempt(row[next_idx:], template[1:]) + (
            attempt(row[1:], template)
            if row[0] == '?'
            else 0
        )
    elif row[0] == '#':
            return 0
    else:
        return attempt(row[1:], template)


async def calculate_combinations(record: Record):
    return attempt(record.row, record.groups)


def part1(input_lines: List[str]) -> int:
    records = parse_input(input_lines)
    return sum(attempt(record.row, record.groups) for record in records)


def part2(input_lines: List[str]) -> int:
    records = map(
        lambda rec: Record(
            '?'.join((rec.row,) * 5), rec.groups * 5
        ),
        parse_input(input_lines)
    )

    tasks = []
    loop = asyncio.get_event_loop()
    for record in records:
        task = loop.create_task(calculate_combinations(record))
        tasks.append(task)

    results = loop.run_until_complete(asyncio.gather(*tasks))
    return sum(results)
