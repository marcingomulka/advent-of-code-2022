import sys
from collections import deque

lines = []
for line in sys.stdin:
    lines.append(line)

char_list = lines[0]
buffer_p1 = deque()
p1_result = 0
for i in range(len(char_list)):
    char = char_list[i]
    if len(buffer_p1) == 4 and len(set(buffer_p1)) == 4:
        p1_result = i
        break
    else:
        if len(buffer_p1) == 4:
            buffer_p1.popleft()
        buffer_p1.append(char)

buffer_p2 = deque()
p2_result = 0
for i in range(len(char_list)):
    char = char_list[i]
    if len(buffer_p2) == 14 and len(set(buffer_p2)) == 14:
        p2_result = i
        break
    else:
        if len(buffer_p2) == 14:
            buffer_p2.popleft()
        buffer_p2.append(char)

print("part1: ", p1_result)
print("part2: ", p2_result)
