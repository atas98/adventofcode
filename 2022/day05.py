from collections import deque, namedtuple

moves_tuple = namedtuple('moves_tuple', 'count from_pos to_pos')


def format_moves(moves_raw: list[str]) -> list[tuple[int, int, int]]:
    moves = []
    for move in moves_raw:
        _, count, _, from_pos, _, to_pos = move.split()
        moves.append(moves_tuple(int(count), int(from_pos), int(to_pos)))
    return moves


input_data: list[str] = open('./2022/day05_input.txt').read().splitlines()
split_point: int = input_data.index('')
storage_raw: list[str] = input_data[:split_point - 1]
storage_indexes = [i for i, char in enumerate(input_data[split_point - 1]) if char != ' ']
storage = [deque() for _ in range(len(storage_indexes))]
for row in storage_raw:
    for i, idx in enumerate(storage_indexes):
        if row[idx] == ' ':
            continue
        storage[i].appendleft(row[idx])

moves_raw: list[str] = input_data[split_point + 1:]
moves = format_moves(moves_raw)

# Part 1
for count, from_pos, to_pos in moves:
    for _ in range(count):
        storage[to_pos - 1].append(storage[from_pos - 1].pop())

# Part 2
for count, from_pos, to_pos in moves:
    reg = deque()
    for _ in range(count):
        if not storage[from_pos - 1]:
            break
        reg.append(storage[from_pos - 1].pop())
    reg.reverse()
    storage[to_pos - 1].extend(reg)


print(''.join(stack[-1] for stack in storage))
