from enum import Enum
from functools import cache, reduce
from itertools import groupby, islice, pairwise
from typing import Callable, Iterable, List, Self

import numpy as np


CellType = Enum(
    'CellType', (
        'GROUND',
        'PIPE_NW',
        'PIPE_NE',
        'PIPE_SW',
        'PIPE_SE',
        'VERTICAL',
        'HORIZONTAL',
        'START',
    )
)


class Node:
    def __init__(self, x: int, y: int, cell: str):
        self.x: int = x
        self.y: int = y
        self.type: CellType = self.get_cell_type(cell)

    def __repr__(self):
        return f"Node({self.x}, {self.y}, {self.type})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    @staticmethod
    def get_cell_type(cell: str) -> CellType:
        match cell:
            case ".":
                return CellType.GROUND
            case "|":
                return CellType.VERTICAL
            case "-":
                return CellType.HORIZONTAL
            case "L":
                return CellType.PIPE_NE
            case "J":
                return CellType.PIPE_NW
            case "7":
                return CellType.PIPE_SW
            case "F":
                return CellType.PIPE_SE
            case "S":
                return CellType.START
            case _:
                raise ValueError(f"Unknown cell type {cell}")

    def is_connected(self, other: Self):
        # For start cell
        if self.y == other.y:
            if self.x == other.x + 1:
                return self.type in (CellType.PIPE_NW, CellType.PIPE_SW,
                                          CellType.HORIZONTAL, CellType.START)
            elif self.x == other.x - 1:
                return self.type in (CellType.PIPE_NE, CellType.PIPE_SE,
                                          CellType.HORIZONTAL, CellType.START)
        elif self.x == other.x:
            if self.y == other.y + 1:
                return self.type in (CellType.PIPE_NW, CellType.PIPE_NE,
                                          CellType.VERTICAL, CellType.START)
            elif self.y == other.y - 1:
                return self.type in (CellType.PIPE_SW, CellType.PIPE_SE,
                                          CellType.VERTICAL, CellType.START)
        return False

    def get_next(self, pipe_map: List[List[Self]], prev_cell: Self | None = None
                 ) -> Self:
        connected_coords = filter(
            lambda coords: 0 <= coords[0] < len(pipe_map[0]) \
                and 0 <= coords[1] < len(pipe_map),
            (
                (self.x, self.y - 1),
                (self.x + 1, self.y),
                (self.x, self.y + 1),
                (self.x - 1, self.y),
            )
        )
        for cell in (pipe_map[y][x] for x, y in connected_coords):
            # Check for out of bounds
            if cell == prev_cell:
                continue

            if cell.is_connected(self) and self.is_connected(cell) \
                    and cell != prev_cell:
                return cell

        return None


def parse_input(input_lines: List[str]) -> Iterable[Iterable[Node]]:
    return [
        [Node(x, y, cell) for x, cell in enumerate(line)]
        for y, line in enumerate(input_lines)
    ]


def get_loop(pipe_map: List[List[Node]]) -> List[Node]:
    start = next(
        node
        for row in pipe_map for node in row
        if node.type == CellType.START
    )
    loop = [start, start.get_next(pipe_map)]
    next_cell = None
    while next_cell != start:
        next_cell = loop[-1].get_next(pipe_map, prev_cell=loop[-2])

        if not next_cell:
            raise ValueError("No next cell")

        loop.append(next_cell)
    return loop


def print_loop(pipe_map: List[List[Node]], highlight: Callable[[Node], str] = None):
    if not highlight:
        highlight = lambda node: "X"
    for y, row in enumerate(pipe_map):
        for x, cell in enumerate(row):
            print(highlight(cell), end="")
        print()


def part1(input_lines: List[str]) -> int:
    pipe_map = parse_input(input_lines)
    loop = get_loop(pipe_map)
    return len(loop) // 2


def area(loop: List[Node]) -> int:
    # Shoelace formula
    return abs(reduce(
        lambda acc, nodes: acc + nodes[0].x * nodes[1].y - nodes[0].y * nodes[1].x,
        pairwise(loop + loop[:1]),
        0,
    )) // 2


def part2(input_lines: List[str]) -> int:
    pipe_map = parse_input(input_lines)
    loop = get_loop(pipe_map)[:-1]

    # Pick's theorem
    return area(loop) + 1 - len(loop) // 2
