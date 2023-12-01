with open("day01_input.txt", "r") as file:
    lines = file.readlines()

calories = []
while '\n' in lines:
    idx = lines.index('\n')
    calories.append(sum([int(line) for line in lines[0:idx]]))
    lines = lines[idx+1:]

print(f"Part 1: {max(calories)}")
print(f"Part 2: {sum(sorted(calories)[-3:])}")
