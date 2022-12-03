import sys


def letter_value(letter):
    val = 0
    if 'z' >= letter >= 'a':
        val = ord(letter) - ord('a') + 1
    elif 'Z' >= letter >= 'A':
        val = ord(letter) - ord('A') + 27
    return val


def group_intersection(group):
    group_common = group[0].intersection(group[1], group[2])
    if len(group_common) != 1:
        print("error, group common not equal to 1", group)
        exit(-1)
    return group_common


lines = []
for line in sys.stdin:
    lines.append(line.strip())

group = []
p1_sum = 0
p2_sum = 0
for line in lines:
    line_size = len(line)
    first = {*line[:line_size // 2]}
    second = {*line[line_size // 2:]}

    common = first.intersection(second)
    if len(common) != 1:
        print("error, intersection not equal to 1", line)
        exit(-1)
    p1_sum += letter_value(common.pop())

    if len(group) < 3:
        group.append({*line})
    else:
        group_common = group_intersection(group)
        p2_sum += letter_value(group_common.pop())
        group = [{*line}]

group.append({*lines[-1]})
group_common = group_intersection(group)
p2_sum += letter_value(group_common.pop())

print("part1: ", p1_sum)
print("part2: ", p2_sum)
