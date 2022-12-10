import sys

CYCLES = {"noop": 1, "addx": 2}
STEPS = {20, 60, 100, 140, 180, 220}
THRESHOLDS = {40, 80, 120, 160, 200, 240}


class Instruction:
    def __init__(self, instruction, value):
        self.instruction = instruction
        self.value = value

    def __repr__(self):
        return "(" + self.instruction + "): " + str(self.value)


lines = []
for line in sys.stdin:
    lines.append(line.strip())
instructions = []
for line in lines:
    chunks = line.split()
    if len(chunks) == 2:
        instructions.append(Instruction(chunks[0], int(chunks[1])))
    else:
        instructions.append((Instruction(chunks[0], 0)))
cycles = 1
register_x = 1
p1_result = 0
row = 0
col = 0
screen = []
for i in range(6):
    screen.append(["."] * 40)
for instr in instructions:
    for i in range(CYCLES[instr.instruction]):
        if col in {register_x, register_x + 1, register_x - 1}:
            screen[row][col] = "#"
        col += 1
        if cycles in STEPS:
            p1_result += cycles * register_x
        if cycles in THRESHOLDS:
            row += 1
            col = 0
        cycles += 1
    if instr.instruction == "addx":
        register_x += instr.value
print("part1:", p1_result)
print("part2:")
for r in screen:
    print("".join(r))
