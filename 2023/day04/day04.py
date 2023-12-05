from functools import cache
from typing import List, Tuple, Set


def parse_card(line: str) -> Tuple[List[int], Set[int]]:
    number_pull, winning_numbers = line.split(': ')[1].split(' | ')
    return (int (number) for number in number_pull.split()), \
        set(int(number) for number in winning_numbers.split())


def part1(input_lines: List[str]) -> int:
    return sum(
        int(2 ** (sum(number in winning for number in numbers) - 1))
        for numbers, winning in (
            parse_card(line) for line in input_lines
        )
    )



def part2(input_lines: List[str]) -> int:

    @cache
    def calc_amount(card_idx: int) -> int:
        if not points[card_idx]:
            return 1
        winning = points[card_idx] \
            if card_idx + points[card_idx] < len(points) \
            else len(points) - card_idx
        return sum(
            calc_amount(i) for i in range(card_idx + 1, card_idx + winning + 1)
        ) + 1

    points = list(
        sum(number in winning for number in numbers)
        for numbers, winning in (
            parse_card(line) for line in input_lines
        )
    )

    return sum(calc_amount(i) for i in range(len(points)))
