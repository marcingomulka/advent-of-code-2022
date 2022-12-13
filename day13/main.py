import sys
from functools import cmp_to_key


def parse_packet(line):
    stack = []
    elements = []
    chars = [*line]
    num_str = ""
    for char in chars:
        if char == "[":
            stack.append(elements)
            elements = []
        elif char == "]":
            if len(num_str) > 0:
                elements.append(int(num_str))
                num_str = ""
            outer_elements = stack.pop()
            outer_elements.append(elements)
            elements = outer_elements
        elif char == ",":
            if len(num_str) > 0:
                elements.append(int(num_str))
                num_str = ""
        else:
            num_str += char
    return elements[0]


def compare(list1, list2):
    size = min(len(list1), len(list2))
    for i in range(size):
        e1 = list1[i]
        e2 = list2[i]
        if not isinstance(e1, list) and not isinstance(e2, list):
            if e1 != e2:
                return e1 - e2
        else:
            if not isinstance(e1, list):
                e1 = [e1]
            if not isinstance(e2, list):
                e2 = [e2]
            equal = compare(e1, e2)
            if equal != 0:
                return equal
    return len(list1) - len(list2)


lines = []
for line in sys.stdin:
    lines.append(line.strip())

packet_pairs = []
p_pair = []
full_list = []
for line in lines:
    if len(line) > 0:
        p_pair.append(parse_packet(line))
    else:
        packet_pairs.append((p_pair[0], p_pair[1]))
        full_list.append(p_pair[0])
        full_list.append(p_pair[1])
        p_pair = []
packet_pairs.append((p_pair[0], p_pair[1]))
full_list.append(p_pair[0])
full_list.append(p_pair[1])

p1_result = 0
for i in range(len(packet_pairs)):
    pair = packet_pairs[i]
    if compare(pair[0], pair[1]) < 0:
        p1_result += i + 1
print("part1:", p1_result)

full_list.append([[2]])
full_list.append([[6]])
sorted_list = sorted(full_list, key=cmp_to_key(compare))
x = 0
y = 0
for i in range(len(sorted_list)):
    if sorted_list[i] == [[2]]:
        x = i + 1
    elif sorted_list[i] == [[6]]:
        y = i + 1
print("part2:", x * y)


