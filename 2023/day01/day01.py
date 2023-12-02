from typing import List


def part1(input_lines: List[str]) -> int:
    def first_digit(line: str) -> str:
        return next(char for char in line if char.isdigit())

    return sum(
        int(f'{first_digit(line)}{first_digit(line[::-1])}')
        for line in input_lines
    )


def part2(input_lines: List[str]) -> int:
    DIGITS = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
    }

    def first_digit_or_str(line: str, reverse: bool = False) -> str:
        for i, char in enumerate(line):
            if char.isdigit():
                return char
            for digit_str in DIGITS:
                if line[i:].startswith(digit_str[::-1 if reverse else 1]):
                    return DIGITS[digit_str]

    return sum(
        int(f'{first_digit_or_str(line)}{first_digit_or_str(line[::-1], reverse=True)}')
        for line in input_lines
    )