import sys


class Rock:
    def __init__(self, width, height, blocks):
        self.blocks = []
        for i in range(height):
            row = []
            for j in range(width):
                if (i, j) in blocks:
                    row.append("@")
                else:
                    row.append(".")
            self.blocks.append(row)
        self.width = width
        self.height = height

    def can_float(self, move, board, pos):
        move_x = 1
        if move == "<":
            move_x = -1
        return self.is_blocked((pos[0], pos[1] + move_x), board)

    def can_fall(self, board, pos):
        return self.is_blocked((pos[0] - 1, pos[1]), board)

    def is_blocked(self, pos, board):
        if pos[0] < 0 or pos[1] < 0 or pos[1] + self.width > 7:
            return False
        for i in range(self.height):
            for j in range(self.width):
                if self.blocks[i][j] == "@" and board[pos[0] - i][pos[1] + j] == "#":
                    return False
        return True

    @staticmethod
    def float_rock(move, pos):
        move_x = 1
        if move == "<":
            move_x = -1
        return pos[0], pos[1] + move_x

    def settle(self, pos, board):
        for i in range(self.height):
            for j in range(self.width):
                if self.blocks[i][j] == "@":
                    board[pos[0] - i][pos[1] + j] = "#"

    def __repr__(self):
        str = ""
        for row in self.blocks:
            str += "".join(row)
            str += "\n"
        return str


def simulate_tetris(shapes, moves, board, step_range):
    top = -1
    wind = 0
    for i in step_range:
        rock = shapes[i % len(shapes)]
        new_row = top + 3 + rock.height
        if len(board) < new_row + 1:
            for j in range(new_row + 1 - len(board)):
                board.append(["."] * 7)

        settled = False
        pos = (new_row, 2)
        while not settled:
            move = moves[wind % len(moves)]
            pos, settled = move_rock(board, move, pos, rock)
            wind += 1
        if pos[0] > top:
            top = pos[0]
    return top + 1


def move_rock(board, move, pos, rock):
    settled = False
    if rock.can_float(move, board, pos):
        pos = rock.float_rock(move, pos)
    if rock.can_fall(board, pos):
        pos = (pos[0] - 1, pos[1])
    else:
        rock.settle(pos, board)
        settled = True
    return pos, settled


lines = []
for line in sys.stdin:
    lines.append(line.strip())

moves = [*lines[0]]
board = [["."] * 7]
shapes = [Rock(4, 1, {(0, 0), (0, 1), (0, 2), (0, 3)}),
          Rock(3, 3, {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)}),
          Rock(3, 3, {(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)}),
          Rock(1, 4, {(0, 0), (1, 0), (2, 0), (3, 0)}),
          Rock(2, 2, {(0, 0), (0, 1), (1, 0), (1, 1)})
          ]
print("part1:", simulate_tetris(shapes, moves, board, range(0, 2022)))

# after some empirical pattern occurrence matching, found a cycle in the tetris tower
CYCLE_TOWER_HEIGHT = 2738
CYCLE_LEN = 1720

cycle_begin = 1000000000000 - (1000000000000 // CYCLE_LEN) * CYCLE_LEN
total_cycles = (1000000000000 - cycle_begin) // CYCLE_LEN
board = [["."] * 7]

remainder = simulate_tetris(shapes, moves, board, range(0, cycle_begin))
print("part2:", CYCLE_TOWER_HEIGHT * total_cycles + remainder)
