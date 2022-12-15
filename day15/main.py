import sys


def manhattan(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])



lines = []
for line in sys.stdin:
    lines.append(line.strip())

bottom = 0
top = sys.maxsize
left = sys.maxsize
right = 0
sensors = set()
beacons = set()
ranges = set()
dists = []
for line in lines:
    chunks = line.split()
    sensor_x = int(chunks[2].replace("x=", "").replace(",", ""))
    sensor_y = int(chunks[3].replace("y=", "").replace(":", ""))
    beacon_x = int(chunks[8].replace("x=", "").replace(",", ""))
    beacon_y = int(chunks[9].replace("y=", ""))
    sensors.add((sensor_x, sensor_y))
    beacons.add((beacon_x, beacon_y))
    dist = manhattan((sensor_x, sensor_y), (beacon_x, beacon_y))
    dists.append(((sensor_x, sensor_y), dist))
for pair in dists:
    sensor = pair[0]
    dist = pair[1]
    if sensor[1] - dist - 1 <= 2000000 <= sensor[1] + dist + 1:
        for x in range(sensor[0] - dist - 1, sensor[0] + dist + 1):
            #for y in range(sensor[1] - dist - 1, sensor[1] + dist + 1):
            y = 2000000
            if manhattan(sensor, (x, y)) <= dist and (x, y) not in sensors and (x, y) not in beacons:
                ranges.add((x, y))
p1_result = 0
for point in ranges:
    if point[1] == 2000000:
        p1_result += 1
#p1_result.sort(key=lambda x: x[0])
#for p in p1_result:
#    print(p)
print("part1:", p1_result)
