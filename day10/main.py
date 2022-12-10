import sys

CYCLES = {"noop": 1, "addx": 2}
STEPS = {20, 60, 100, 140, 180, 220}
THRESHOLDS = {40, 80, 120, 160, 200, 240}


class Instruction:
    def __init__(self, command, value):
        self.command = command
        self.value = value

    def __repr__(self):
        return "(" + self.command + "): " + str(self.value)


lines = []
for line in sys.stdin:
    lines.append(line.strip())
instr_list = []
for line in lines:
    chunks = line.split()
    if len(chunks) == 2:
        instr_list.append(Instruction(chunks[0], int(chunks[1])))
    else:
        instr_list.append(Instruction(chunks[0], 0))

screen = []
for i in range(6):
    screen.append(["."] * 40)
cycle = 1
x = 1
p1_result = 0
row = 0
col = 0
for instr in instr_list:
    for i in range(CYCLES[instr.command]):
        if col in {x, x + 1, x - 1}:
            screen[row][col] = "#"
        col += 1
        if cycle in STEPS:
            p1_result += cycle * x
        if cycle in THRESHOLDS:
            row += 1
            col = 0
        cycle += 1
    if instr.command == "addx":
        x += instr.value
print("part1:", p1_result)
print("part2:")
for r in screen:
    print("".join(r))
