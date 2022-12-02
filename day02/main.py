import sys

MY_POINTS = {"X": 1, "Y": 2, "Z": 3}


def compare(opponent, me):
    if me == "Z" and opponent == "B":
        return True
    elif me == "X" and opponent == "C":
        return True
    elif me == "Y" and opponent == "A":
        return True
    else:
        return False


def is_draw(opponent, me):
    if me == "X" and opponent == "A":
        return True
    elif me == "Y" and opponent == "B":
        return True
    elif me == "Z" and opponent == "C":
        return True
    else:
        return False


def calculate_turn(opponent, me):
    if me == "X":  # loose
        if opponent == "A":
            return "Z"
        elif opponent == "B":
            return "X"
        else:
            return "Y"
    elif me == "Y":  # draw
        if opponent == "A":
            return "X"
        elif opponent == "B":
            return "Y"
        else:
            return "Z"
    elif me == "Z":  # win
        if opponent == "A":
            return "Y"
        elif opponent == "B":
            return "Z"
        else:
            return "X"


def calculate_score(opponent, me):
    score = 0
    if compare(opponent, me):
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
