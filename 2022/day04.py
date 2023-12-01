assignments_file = open('/day04_input.txt')
assignments: list[list[int]] = [
    [[int(asmt) for asmt in elfs.split('-')] for elfs in line.split(',')]
    for line in assignments_file.readlines()
    if line
]


# Part 1
contains_count = sum(
    (e1_min in range(e2_min, e2_max + 1) and e1_max in range(e2_min, e2_max + 1))
    or (e2_min in range(e1_min, e1_max + 1) and e2_max in range(e1_min, e1_max + 1))
    for (e1_min, e1_max), (e2_min, e2_max) in assignments
)

# Part 2
intersect_count = sum(
    e1_min in range(e2_min, e2_max + 1) or e1_max in range(e2_min, e2_max + 1)
    or e2_min in range(e1_min, e1_max + 1) or e2_max in range(e1_min, e1_max + 1)
    for (e1_min, e1_max), (e2_min, e2_max) in assignments
)


print(f'Part 1: {contains_count}')
print(f'Part 2: {intersect_count}')
