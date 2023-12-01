from typing import Generator


with open("day03_input.txt", "r") as file:
    lines = [line for line in file.read().split('\n') if line]


def get_priority(item: str) -> int:
    if item.islower():
        return ord(item) - ord('a') + 1
    return ord(item) - ord('A') + 27


def split_by_3(items: list) -> Generator[str, None, None]:
    for i in range(0, len(items), 3):
        yield items[i:i + 3]


# Part 1
res = 0
for line in lines:
    items = list(line)
    compartment_size = len(items) // 2
    intersection = set(items[:compartment_size]).intersection(set(items[compartment_size:]))
    res += sum(get_priority(item) for item in intersection)
print(res)


# Part 2
res = 0
for l1, l2, l3 in split_by_3(lines):
    intersection = set(l1) & set(l2) & set(l3)
    res += sum(get_priority(item) for item in intersection)
print(res)
