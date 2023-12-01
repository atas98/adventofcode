FIGURE_SCORE = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}


with open("day02_input.txt", "r") as file:
    lines = file.read().split('\n')

# Part 1
score = 0
for line in lines:
    if not line:
        continue
    fig1, fig2 = line.split()
    score += FIGURE_SCORE[fig2]
    if fig1 == 'A':
        score += fig2 == 'X' and 3 or fig2 == 'Z' and 0 or fig2 == 'Y' and 6
    elif fig1 == 'B':
        score += fig2 == 'X' and 0 or fig2 == 'Z' and 6 or fig2 == 'Y' and 3
    elif fig1 == 'C':
        score += fig2 == 'X' and 6 or fig2 == 'Z' and 3 or fig2 == 'Y' and 0

print(f"Part 1: {score}")


# Part 2
score = 0
for line in lines:
    if not line:
        continue
    fig1, res = line.split()

    if res == 'X':
        score += 0
        fig2 = fig1 == 'A' and 'Z' or fig1 == 'B' and 'X' or fig1 == 'C' and 'Y'
    elif res == 'Y':
        score += 3
        fig2 = fig1 == 'A' and 'X' or fig1 == 'B' and 'Y' or fig1 == 'C' and 'Z'
    elif res == 'Z':
        score += 6
        fig2 = fig1 == 'A' and 'Y' or fig1 == 'B' and 'Z' or fig1 == 'C' and 'X'
    score += FIGURE_SCORE[fig2]

print(f"Part 2: {score}")
