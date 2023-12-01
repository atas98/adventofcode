from itertools import islice


def window(seq, n):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


input_file = open('./2022/day06_input.txt')
signal = input_file.read().rstrip('\n')

for i, letters in enumerate(window(signal, 4)):
    if len(set(letters)) == 4:
        print(f'Part 1: {i + 4}')
        break

for i, letters in enumerate(window(signal, 14)):
    if len(set(letters)) == 14:
        print(f'Part 2: {i + 14}')
        break
