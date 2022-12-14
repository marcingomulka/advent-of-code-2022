import sys
from copy import deepcopy


def draw_line(cave_line, cave, offset):
    start = cave_line[0]
    for point in cave_line[1:]:
        cave[point[1]][point[0] - offset] = "#"
        cave[start[1]][start[0] - offset] = "#"
        if start[0] == point[0]:
            if point[1] - start[1] > 0:
                for i in range(abs(point[1] - start[1])):
                    cave[start[1] + i][start[0] - offset] = "#"
            else:
                for i in range(abs(point[1] - start[1])):
                    cave[point[1] + i][point[0] - offset] = "#"
        elif start[1] == point[1]:
            if point[0] - start[0] > 0:
                for i in range(abs(point[0] - start[0])):
                    cave[start[1]][start[0] + i - offset] = "#"
            else:
                for i in range(abs(point[0] - start[0])):
                    cave[point[1]][point[0] + i - offset] = "#"
        start = point


def is_void(target, cave):
    if target[1] < 0:
        return True
    if target[1] >= len(cave):
        return True
    if target[0] < 0:
        return True
    if target[0] >= len(cave[0]):
        return True
    if cave[target[1]][target[0]] == ".":
        return True
    return False


def fall_sand(sand_src, cave):
    sand = sand_src
    over_fill = True
    while sand[1] < len(cave):
        if is_void((sand[0], sand[1] + 1), cave):
            sand = (sand[0], sand[1] + 1)
        elif is_void((sand[0] - 1, sand[1] + 1), cave):
            sand = (sand[0] - 1, sand[1] + 1)
        elif is_void((sand[0] + 1, sand[1] + 1), cave):
            sand = (sand[0] + 1, sand[1] + 1)
        elif 0 <= sand[0] < len(cave[0]) and sand[1] < len(cave) and cave[sand[1]][sand[0]] == ".":
            cave[sand[1]][sand[0]] = "o"
            over_fill = False
            break
        else:
            break
    if over_fill:
        print(offset + sand[0], sand[1])
    return over_fill


def print_cave(cave):
    for row in cave:
        print("".join(row))


lines = []
for line in sys.stdin:
    lines.append(line.strip())

cave_lines = []
depth = 0
left = sys.maxsize
right = 0
for line in lines:
    points_str = line.split("->")
    line_points = []
    for point_str in points_str:
        coords = point_str.strip().split(",")
        x = int(coords[0])
        y = int(coords[1])
        line_points.append((x, y))
        if y > depth:
            depth = y
        if x < left:
            left = x
        if x > right:
            right = x
    cave_lines.append(line_points)

cave = []
cols_num = right - left + 1
offset = left
sand_src = (500 - offset, 0)
for i in range(depth + 1):
    cave.append(["."] * cols_num)

for cave_line in cave_lines:
    draw_line(cave_line, cave, offset)
cave[sand_src[1]][sand_src[0]] = "+"

filled = False
p1_result = 0
while not filled:
    filled = fall_sand(sand_src, cave)
    if not filled:
        p1_result += 1
#print_cave(cave)
print("part1:", p1_result)

new_cave = []
for i in range(depth + 1):
    new_cave.append(["."] * 1000)
    if i < len(cave):
        for j in range(cols_num):
            if cave[i][j] == "#":
                new_cave[i][j + offset] = "#"
new_cave.append(["."] * 1000)
new_cave.append(["#"] * 1000)

p2_result = 0
filled = False
sand_src = (500, 0)
while not filled:
    filled = fall_sand(sand_src, new_cave)
    if not filled:
        p2_result += 1
#print_cave(new_cave)
print("part2:", p2_result)

