from itertools import cycle
import math
from typing import Callable, Dict, List, Self, Tuple


class Node:
    def __init__(self, name: str, left: Self | None = None, right: Self | None = None):
        self.name = name
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return (f'Node({self.name}, '
                f'{self.left and self.left.name}, '
                f'{self.right and self.right.name})')


def parse_input(input_lines: List[str]) -> Tuple[str, Dict[str, Node]]:
    steps = input_lines[0]
    # Parse lines `### = (###, ###)` into a tree of nodes
    nodes = {}
    for line in input_lines[2:]:
        name, children = line.split(' = ')
        left, right = children[1:-1].split(', ')

        if left not in nodes:
            nodes[left] = Node(left)
        if right not in nodes and right != name:
            nodes[right] = Node(right)

        left, right = nodes[left], nodes[right]

        if name not in nodes:
            node = Node(name)
            nodes[name] = node
        else:
            node = nodes[name]
        node.left = left
        node.right = right

    return steps, nodes


def find_path_len(start: Node, is_end: Callable[[Node], bool], path: str) -> int:
    steps = 0
    cursor = start
    for direction in cycle(path):
        if is_end(cursor):
            return steps
        if direction == 'L':
            if not cursor.left:
                raise ValueError('Cursor cannot move left')
            cursor = cursor.left
            steps += 1
        elif direction == 'R':
            if not cursor.right:
                raise ValueError('Cursor cannot move right')
            cursor = cursor.right
            steps += 1


def part1(input_lines: List[str]) -> int:
    directions, nodes = parse_input(input_lines)
    start, end = nodes['AAA'], nodes['ZZZ']
    return find_path_len(
        start,
        lambda node: node == end,
        directions
    )


def part2(input_lines: List[str]) -> int:
    directions, nodes = parse_input(input_lines)
    starts = filter(lambda node: node.name.endswith('A'), nodes.values())
    ends = set(filter(lambda node: node.name.endswith('Z'), nodes.values()))

    return math.lcm(*(
        find_path_len(start, lambda node: node in ends, directions)
        for start in starts
    ))
