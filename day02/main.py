import sys

MY_POINTS = {"X": 1, "Y": 2, "Z": 3}

WIN_PAIRS = {"A": "Y", "B": "Z", "C": "X"}
DRAW_PAIRS = {"A": "X", "B": "Y", "C": "Z"}
LOSE_PAIRS = {"A": "Z", "B": "X", "C": "Y"}


def is_win(opponent, me):
    if WIN_PAIRS[opponent] == me:
        return True
    else:
        return False


def is_draw(opponent, me):
    if DRAW_PAIRS[opponent] == me:
        return True
    else:
        return False


def calculate_turn(opponent, me):
    if me == "X":  # loose
        return LOSE_PAIRS[opponent]
    elif me == "Y":  # draw
        return DRAW_PAIRS[opponent]
    elif me == "Z":  # win
        return WIN_PAIRS[opponent]


def calculate_score(opponent, me):
    score = 0
    if is_win(opponent, me):
        score += 6
    elif is_draw(opponent, me):
        score += 3
    score += MY_POINTS[me]
    return score


lines = []
for line in sys.stdin:
    lines.append(line)

score = 0
part2_score = 0

for line in lines:
    chunks = line.split()
    opponent = chunks[0]
    me = chunks[1]

    score += calculate_score(opponent, me)
    my_strategy = calculate_turn(opponent, me)
    part2_score += calculate_score(opponent, my_strategy)

print("part1: ", score)
print("part2: ", part2_score)
