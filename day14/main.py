import sys


def draw_line(cave_line, cave, offset):
    start = cave_line[0]
    for point in cave_line[1:]:
        cave[point[1]][point[0] - offset] = "#"
        cave[start[1]][start[0] - offset] = "#"
        if start[0] == point[0]:
            draw_vertical(cave, offset, point, start)
        elif start[1] == point[1]:
            draw_horizontal(cave, offset, point, start)
        start = point


def draw_horizontal(cave, offset, point, start):
    if point[0] - start[0] > 0:
        for i in range(abs(point[0] - start[0])):
            cave[start[1]][start[0] + i - offset] = "#"
    else:
        for i in range(abs(point[0] - start[0])):
            cave[point[1]][point[0] + i - offset] = "#"


def draw_vertical(cave, offset, point, start):
    if point[1] - start[1] > 0:
        for i in range(abs(point[1] - start[1])):
            cave[start[1] + i][start[0] - offset] = "#"
    else:
        for i in range(abs(point[1] - start[1])):
            cave[point[1] + i][point[0] - offset] = "#"


def can_fall(target, cave):
    return target[1] < 0 or target[1] >= len(cave) or target[0] < 0 \
           or target[0] >= len(cave[0]) or cave[target[1]][target[0]] == "."


def fall_sand(sand_src, cave):
    sand = sand_src
    while sand[1] < len(cave):
        if can_fall((sand[0], sand[1] + 1), cave):
            sand = (sand[0], sand[1] + 1)
        elif can_fall((sand[0] - 1, sand[1] + 1), cave):
            sand = (sand[0] - 1, sand[1] + 1)
        elif can_fall((sand[0] + 1, sand[1] + 1), cave):
            sand = (sand[0] + 1, sand[1] + 1)
        elif 0 <= sand[0] < len(cave[0]) and sand[1] < len(cave) and cave[sand[1]][sand[0]] == ".":
            cave[sand[1]][sand[0]] = "o"
            return False
        else:
            break
    return True


def pour(cave, src):
    overfill = False
    result = 0
    while not overfill:
        overfill = fall_sand(src, cave)
        if not overfill:
            result += 1
    return result


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
row_num = depth + 1
offset = left
for i in range(row_num):
    cave.append(["."] * cols_num)
for cave_line in cave_lines:
    draw_line(cave_line, cave, offset)

sand_src = (500 - offset, 0)
cave[sand_src[1]][sand_src[0]] = "+"
print("part1:", pour(cave, sand_src))
#print_cave(cave)

new_cave = []
for i in range(row_num):
    new_cave.append(["."] * 1000)
    for j in range(cols_num):
        if cave[i][j] == "#":
            new_cave[i][j + offset] = "#"
new_cave.append(["."] * 1000)
new_cave.append(["#"] * 1000)
print("part2:", pour(new_cave, (500, 0)))
#print_cave(new_cave)