import sys
from collections import deque


class Move:
    def __init__(self, count, start_position, target_position):
        self.count = count
        self.start_position = start_position
        self.target_position = target_position


def move_crate_p1(stacks, move):
    for x in range(move.count):
        c = stacks[move.start_position - 1].pop()
        stacks[move.target_position - 1].append(c)


def move_crate_p2(stacks, move):
    list = []
    for x in range(0, move.count):
        list.append(stacks[move.start_position - 1].pop())
    list.reverse()
    for l in list:
        stacks[move.target_position - 1].append(l)


lines = []
for line in sys.stdin:
    lines.append(line)

row = []
rows = []
moves = []
for line in lines:
    if not line.startswith("move"):
        iter = 1
        while iter < len(line):
            row.append(line[iter])
            iter += 4
        rows.append(row)
        row = []
    else:
        chunks = line.split()
        moves.append(Move(int(chunks[1]), int(chunks[3]), int(chunks[5])))
rows.reverse()
stacks_p1 = []
stacks_p2 = []
stacks_num = len(rows[1])
for i in range(stacks_num):
    stacks_p1.append(deque())
    stacks_p2.append(deque())
for row in rows:
    if len(row) > 0 and row[0] != '1':
        index = 0
        for char in row:
            if char != ' ':
                stacks_p1[index].append(row[index])
                stacks_p2[index].append(row[index])
            index += 1
for move in moves:
    move_crate_p1(stacks_p1, move)
    move_crate_p2(stacks_p2, move)

result = ""
for s in stacks_p1:
    result += s.pop()
result2 = ""
for s in stacks_p2:
    result2 += s.pop()
print("part1: ", result)
print("part2: ", result2)
