import sys


def count_faces_axis_x(zero):
    faces_count = 0
    for k in range(len(space[0][0])):
        for j in range(len(space[0])):
            sum = 0
            pattern = ""
            for i in range(len(space)):
                pattern += space[i][j][k]
            is_zero = True
            for c in pattern:
                if c == "1" and is_zero:
                    sum += 1
                    is_zero = False
                elif c == zero and not is_zero:
                    sum += 1
                    is_zero = True
            if not is_zero:
                sum += 1
            faces_count += sum
    return faces_count


def count_faces_axis_y(zero):
    faces_count = 0
    for i in range(len(space)):
        for k in range(len(space[0][0])):
            sum = 0
            pattern = ""
            for j in range(len(space[0])):
                pattern += space[i][j][k]
            is_zero = True
            for c in pattern:
                if c == "1" and is_zero:
                    sum += 1
                    is_zero = False
                elif c == zero and not is_zero:
                    sum += 1
                    is_zero = True
            if not is_zero:
                sum += 1
            faces_count += sum
    return faces_count


def count_faces_axis_z(zero):
    faces_count = 0
    for i in range(len(space)):
        for j in range(len(space[0])):
            sum = 0
            pattern = ""
            for k in range(len(space[0][0])):
                pattern += space[i][j][k]
            is_zero = True
            for c in pattern:
                if c == "1" and is_zero:
                    sum += 1
                    is_zero = False
                elif c == zero and not is_zero:
                    sum += 1
                    is_zero = True
            if not is_zero:
                sum += 1
            faces_count += sum
    return faces_count


def get_neighbors(cube, space):
    result = []
    x = cube[0]
    y = cube[1]
    z = cube[2]
    if x - 1 >= 0:
        result.append((x - 1, y, z))
    if x + 1 < len(space):
        result.append((x + 1, y, z))
    if y - 1 >= 0:
        result.append((x, y - 1, z))
    if y + 1 < len(space[0]):
        result.append((x, y + 1, z))
    if z - 1 >= 0:
        result.append((x, y, z - 1))
    if z + 1 < len(space[0][0]):
        result.append((x, y, z + 1))
    return result


def fill(start, space):
    queue = [start]
    while len(queue) > 0:
        cube = queue.pop()
        space[cube[0]][cube[1]][cube[2]] = "Z"
        for n in get_neighbors(cube, space):
            if space[n[0]][n[1]][n[2]] == "0":
                queue.append(n)


lines = []
for line in sys.stdin:
    lines.append(line.strip())

max_x = 0
min_x = sys.maxsize
max_y = 0
min_y = sys.maxsize
max_z = 0
min_z = sys.maxsize
cubes = set()
for line in lines:
    chunks = line.split(",")
    cubes.add((int(chunks[0]), int(chunks[1]), int(chunks[2])))
for cube in cubes:
    if cube[0] > max_x:
        max_x = cube[0]
    if cube[0] < min_x:
        min_x = cube[0]
    if cube[1] > max_y:
        max_y = cube[1]
    if cube[1] < min_y:
        min_y = cube[1]
    if cube[2] > max_z:
        max_z = cube[2]
    if cube[2] < min_z:
        min_z = cube[2]

space = []
for i in range(min_x, max_x + 1):
    area = []
    for j in range(min_y, max_y + 1):
        row = []
        for k in range(min_z, max_z + 1):
            if (i, j, k) in cubes:
                row.append("1")
            else:
                row.append("0")
        area.append(row)
    space.append(area)

z_faces = count_faces_axis_z("0")
y_faces = count_faces_axis_y("0")
x_faces = count_faces_axis_x("0")
print("part1", z_faces + x_faces + y_faces)

start = (0, 0, 0)
fill(start, space)

z_faces = count_faces_axis_z("Z")
y_faces = count_faces_axis_y("Z")
x_faces = count_faces_axis_x("Z")
print("part2", z_faces + x_faces + y_faces)
