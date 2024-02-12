from itertools import groupby
from typing import Generator, Iterable, List, Tuple


def parse_input(input_lines: List[str]) -> Iterable[Tuple[Tuple[bool]]]:
    return [tuple(tuple(
            char == '#' for char in line
        ) for line in group)
        for k, group in groupby(input_lines, lambda line: line == '')
        if not k
    ]


def eq_row(data: Tuple[Tuple[bool]], row1: int, row2: int, error: int = 0) -> tuple[bool, bool]:
    res = sum(1 for col in range(len(data[0])) if data[row1][col] == data[row2][col])
    return res in (len(data[0]), len(data[0]) - error), res == len(data[0]) - error


def eq_col(data: Tuple[Tuple[bool]], col1: int, col2: int, error: int = 0) -> tuple[bool, bool]:
    res = sum(1 for row in range(len(data)) if data[row][col1] == data[row][col2])
    return res in (len(data), len(data) - error), res == len(data) - error


def get_pairs(length: int, axis: int) -> Generator[Tuple[int, int], None, None]:
    """ Return pairs of indices that expand from the axis index
        to the length of the data in both directions.
        E.g.: get_pairs(6, 2) -> (2, 3), (1, 4), (0, 5)

    :param int length: length of the data
    :param int axis: axis index
    :yield Generator[Tuple[int, int], None, None]
    """
    # Determine the minimum distance from the axis to the edges
    a = axis
    b = axis + 1
    while a >= 0 and b < length:
        yield a, b
        a -= 1
        b += 1


def check_rows(record, error=0):
    for axis in range(len(record) - 1):
        had_err = False
        for r1, r2 in get_pairs(len(record), axis):
            res, err = eq_row(record, r1, r2, error)
            if not error:
                if not res:
                    break
            else:
                if (axis == 0 or axis == len(record) - 2) and res and not err:
                    break
                if not res and (had_err or not err):
                    break
            had_err = had_err or err
        else:
            if error and not had_err:
                continue
            return (axis + 1) * 100
    return 0


def check_columns(record, error=0):
    for axis in range(len(record[0]) - 1):
        had_err = False
        for c1, c2 in get_pairs(len(record[0]), axis):
            res, err = eq_col(record, c1, c2, error)
            if not error:
                if not res:
                    break
            else:
                if (axis == 0 or axis == len(record[0]) - 2) and res and not err:
                    break
                if not res and (had_err or not err):
                    break
            had_err = had_err or err
        else:
            if error and not had_err:
                continue
            return axis + 1
    return 0


def part1(input_lines: List[str]) -> int:
    records = parse_input(input_lines)
    score = 0

    for record in records:
        score += check_rows(record) or check_columns(record)

    return score


def part2(input_lines: List[str]) -> int:
    records = parse_input(input_lines)
    score = 0

    for i, record in enumerate(records):
        score += check_rows(record, 1) or check_columns(record, 1)

    return score
