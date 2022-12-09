import sys


class Move:
    def __init__(self, direction, steps):
        self.direction = direction
        self.steps = steps

    def one_step(self, pos):
        match self.direction:
            case "U":
                return (pos[0], pos[1] + 1)
            case "D":
                return (pos[0], pos[1] - 1)
            case "L":
                return (pos[0] - 1, pos[1])
            case "R":
                return (pos[0] + 1, pos[1])


def dist(to_follow, knot):
    return max(abs(to_follow[0] - knot[0]), abs(to_follow[1] - knot[1]))


def follow(to_follow, knot):
    dist_x = abs(to_follow[0] - knot[0])
    dist_y = abs(to_follow[1] - knot[1])
    move_x = 0
    move_y = 0
    if dist_x >= 2:
        move_x = 1
        if dist_y > 0:
            move_y = 1
    if dist_y >= 2:
        move_y = 1
        if dist_x > 0:
            move_x = 1
    if to_follow[0] - knot[0] < 0:
        move_x *= -1
    if to_follow[1] - knot[1] < 0:
        move_y *= -1
    return knot[0] + move_x, knot[1] + move_y


lines = []
for line in sys.stdin:
    lines.append(line.strip())
moves = []
for line in lines:
    chunks = line.split()
    moves.append(Move(chunks[0], int(chunks[1])))
head_pos = (0, 0)
knot_positions = [(0, 0)] * 9
p1_trace = set()
p1_trace.add(head_pos)
p2_trace = set()
p2_trace.add(head_pos)
for move in moves:
    for step in range(move.steps):
        head_pos = move.one_step(head_pos)
        to_follow = head_pos
        for i in range(len(knot_positions)):
            knot = knot_positions[i]
            if dist(to_follow, knot) >= 2:
                knot = follow(to_follow, knot)
                if i == 0:
                    p1_trace.add(knot)
                if i == 8:
                    p2_trace.add(knot)
            to_follow = knot
            knot_positions[i] = knot
print("part1:", len(p1_trace))
print("part2: ", len(p2_trace))
