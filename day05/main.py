import sys
from collections import deque


def move_crate(stacks, count, start, target):
    for x in range(count):
        c = stacks[start-1].pop()
        stacks[target-1].append(c)


def move_crate_p2(stacks, count, start, target):
    list = []
    for x in range(0, count):
        list.append(stacks[start-1].pop())
    list.reverse()
    for l in list:
        stacks[target-1].append(l)


lines = []
for line in sys.stdin:
    lines.append(line)

row = []
rows = []

move_counts = []
start_pos = []
target_pos = []

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
        move_counts.append(int(chunks[1]))
        start_pos.append(int(chunks[3]))
        target_pos.append(int(chunks[5]))


rows.reverse()
stacks = []
stacks_p2 = []
stacks_num = len(rows[1])
for i in range(stacks_num):
    stacks.append(deque())
    stacks_p2.append(deque())

for row in rows:
    if len(row) > 0 and row[0] != '1':
        index = 0
        for char in row:
            if char != ' ':
                stacks[index].append(row[index])
                stacks_p2[index].append(row[index])
            index += 1

index = 0
for count in move_counts:
    start = start_pos[index]
    target = target_pos[index]
    move_crate(stacks, count, start, target)
    move_crate_p2(stacks_p2, count, start, target)
    index += 1

result = ""
for s in stacks:
    result += s.pop()
result2 = ""
for s in stacks_p2:
    result2 += s.pop()

print("part1: ", result)
print("part2: ", result2)
