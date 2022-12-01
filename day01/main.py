import sys

lines = []
for line in sys.stdin:
    lines.append(line)

elve = []
elves = []
for line in lines:
    if line == '\n':
        elves.append(sum(elve))
        elve = []
    else:
        elve.append(int(line))
elves.append(sum(elve))

elves.sort(reverse=True)
print(elves)
print("part1: ", elves[0])
print("part2: ", elves[0] + elves[1] + elves[2])

