import sys
from collections import deque


def find_start_packet_pos(char_list, buffer_len):
    buffer = deque()
    result = 0
    for i in range(len(char_list)):
        char = char_list[i]
        if len(buffer) == buffer_len and len(set(buffer)) == buffer_len:
            result = i
            break
        else:
            if len(buffer) == buffer_len:
                buffer.popleft()
            buffer.append(char)
    return result


lines = []
for line in sys.stdin:
    lines.append(line)

p1_result = find_start_packet_pos(lines[0], 4)
p2_result = find_start_packet_pos(lines[0], 14)
print("part1: ", p1_result)
print("part2: ", p2_result)
