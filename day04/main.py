import sys


def build_sequence(range_str):
    bounds = range_str.split("-")
    return set(range(int(bounds[0]), int(bounds[1])+1))


lines = []
for line in sys.stdin:
    lines.append(line.strip())

p1_sum = 0
p2_sum = 0
for line in lines:
    pair = line.split(',')
    range1 = build_sequence(pair[0])
    range2 = build_sequence(pair[1])
    intersect = range1.intersection(range2)
    if intersect == range2 or intersect == range1:
        p1_sum += 1
    if len(intersect) > 0:
        p2_sum += 1

print("part1: ", p1_sum)
print("part2: ", p2_sum)
