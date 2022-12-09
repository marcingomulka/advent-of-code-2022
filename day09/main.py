import sys


class Move:
    def __init__(self, direction, steps):
        self.direction = direction
        self.steps = steps


def move_step_h(pos, direction):
    if direction == "U":
        return (pos[0], pos[1] + 1)
    elif direction == "D":
        return (pos[0], pos[1] - 1)
    elif direction == "L":
        return (pos[0] - 1, pos[1])
    else:
        return (pos[0] + 1, pos[1])


def dist(h_pos, t_pos):
    return max(abs(h_pos[0] - t_pos[0]), abs(h_pos[1] - t_pos[1]))


def follow(t_pos, h_pos):
    dist_x = abs(h_pos[0] - t_pos[0])
    dist_y = abs(h_pos[1] - t_pos[1])
    move_x = 0
    move_y = 0
    if dist_x >= 2:
        move_x = 1
    if dist_y >= 2:
        move_y = 1
    if move_x == 1 and dist_y == 1:
        move_y = 1
    if move_y == 1 and dist_x == 1:
        move_x = 1
    if h_pos[0] - t_pos[0] < 0:
        move_x *= -1
    if h_pos[1] - t_pos[1] < 0:
        move_y *= -1
    result = (t_pos[0] + move_x, t_pos[1] + move_y)
    return result


lines = []
for line in sys.stdin:
    lines.append(line.strip())
moves = []
for line in lines:
    chunks = line.split()
    moves.append(Move(chunks[0], int(chunks[1])))
h_pos = (0, 0)
t_pos = (0, 0)
knot_positions = [(0, 0)] * 9
p1_trace = set()
p1_trace.add(t_pos)
p2_trace = set()
p2_trace.add(h_pos)
for move in moves:
    for step in range(move.steps):
        h_pos = move_step_h(h_pos, move.direction)
        to_follow = h_pos
        for i in range(len(knot_positions)):
            knot = knot_positions[i]
            if dist(to_follow, knot) >= 2:
                knot = follow(knot, to_follow)
                if i == 0:
                    p1_trace.add(knot)
                if i == 8:
                    p2_trace.add(knot)
            to_follow = knot
            knot_positions[i] = knot
print("part1:", len(p1_trace))
print("part2: ", len(p2_trace))
