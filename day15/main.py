import sys
import time
from functools import cmp_to_key


class RangeBound:
    def __init__(self, val, bound):
        self.val = val
        # bound -  "L" for left, "R" for right
        self.bound = bound

    def __repr__(self):
        return self.bound + str(self.val)


def compare_range_bound(bound1, bound2):
    equal = bound1.val - bound2.val
    if equal == 0:
        # if same val, then "L" is before "R"
        return ord(bound1.bound) - ord(bound2.bound)
    else:
        return equal


def find_missing_col(ranges, limit):
    stack = []
    first = ranges[0]
    last = first
    if first.val > 0 or first.bound != "L":
        return 0
    stack.append(first)
    for x in ranges[1:]:
        if x.bound == "R":
            stack.pop()
            last = x
        else:
            stack.append(x)
        if len(stack) == 0 and last.val < limit:
            return last.val + 1
    return -1


def count_ranges(ranges):
    result = 0
    stack = []
    first = ranges[0]
    stack.append(first)
    for x in ranges[1:]:
        if x.bound == "R":
            stack.pop()
            last = x
            if len(stack) == 0:
                result += last.val - first.val
        else:
            if len(stack) == 0:
                first = x
            stack.append(x)
    return result


def manhattan(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])


TEST_RANGE = 21
INPUT_RANGE = 4000001
SELECTED_RANGE = INPUT_RANGE
P1_RANGE = SELECTED_RANGE // 2
lines = []
for line in sys.stdin:
    lines.append(line.strip())

sensor_dist_list = []
p1_result = set()
for line in lines:
    chunks = line.split()
    sensor_x = int(chunks[2].replace("x=", "").replace(",", ""))
    sensor_y = int(chunks[3].replace("y=", "").replace(":", ""))
    beacon_x = int(chunks[8].replace("x=", "").replace(",", ""))
    beacon_y = int(chunks[9].replace("y=", ""))
    dist = manhattan((sensor_x, sensor_y), (beacon_x, beacon_y))
    sensor_dist_list.append(((sensor_x, sensor_y), dist))

start_time = time.time()
# 4M rows with ranges bounds ("L" or "R")
rows = []
for i in range(SELECTED_RANGE):
    rows.append([])
for sensor_dist in sensor_dist_list:
    sensor = sensor_dist[0]
    dist = sensor_dist[1]
    top = sensor[1] - dist
    bottom = sensor[1] + dist

    increment = 0
    for i in range(top, sensor[1] + 1):
        increment += 1
        if i < 0:
            continue
        rows[i].append(RangeBound(sensor[0] - increment + 1, "L"))
        rows[i].append(RangeBound(sensor[0] + increment - 1, "R"))
    for i in range(sensor[1] + 1, bottom + 1):
        increment -= 1
        if i > SELECTED_RANGE - 1:
            break
        rows[i].append(RangeBound(sensor[0] - increment + 1, "L"))
        rows[i].append(RangeBound(sensor[0] + increment - 1, "R"))
print("calculation of ranges done, total rows processed:", len(rows))
print("elapsed time [s]:", time.time() - start_time)

rows[P1_RANGE].sort(key=cmp_to_key(compare_range_bound))
print("part1:", count_ranges(rows[P1_RANGE]))

p2_result = 0
for i in range(len(rows)):
    rows[i].sort(key=cmp_to_key(compare_range_bound))
    ranges = rows[i]
    j = find_missing_col(ranges, SELECTED_RANGE)
    if j >= 0:
        p2_result = j * 4000000 + i
        break
print("part2:", p2_result)
print("elapsed time [s]", time.time() - start_time)
