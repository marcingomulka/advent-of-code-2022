import sys


class Block:
    def __init__(self, width, height, blocks):
        self.block = []
        for i in range(height):
            row = []
            for j in range(width):
                if (i, j) in blocks:
                    row.append("@")
                else:
                    row.append(".")
            self.block.append(row)
        self.width = width
        self.height = height

    def is_blocked(self, pos, board):
        if pos[0] < 0 or pos[1] < 0 or pos[1] + self.width > 7:
            return False
        for i in range(self.height):
            for j in range(self.width):
                if self.block[i][j] == "@" and board[pos[0] - i][pos[1] + j] == "#":
                    return False
        return True

    def settle(self, pos, board):
        for i in range(self.height):
            for j in range(self.width):
                if self.block[i][j] == "@":
                    board[pos[0] - i][pos[1] + j] = "#"

    def __repr__(self):
        str = ""
        for row in self.block:
            str += "".join(row)
            str += "\n"
        return str


def can_float(move, rock, board, pos):
    move_x = 1
    if move == "<":
        move_x = -1
    return rock.is_blocked((pos[0], pos[1] + move_x), board)


def float_rock(move, pos):
    move_x = 1
    if move == "<":
        move_x = -1
    return pos[0], pos[1] + move_x


def can_fall(rock, board, pos):
    return rock.is_blocked((pos[0] - 1, pos[1]), board)


def simulate_tetris(top_idx, wind, shapes, moves, board, step_range):
    for i in step_range:
        rock = shapes[i % len(shapes)]
        settled = False
        new_row = top_idx + 3 + rock.height
        pos = (new_row, 2)
        if len(board) < new_row + 1:
            for j in range(new_row + 1 - len(board)):
                board.append(["."] * 7)
        while not settled:
            move = moves[wind]
            if can_float(move, rock, board, pos):
                pos = float_rock(move, pos)
            if can_fall(rock, board, pos):
                pos = (pos[0] - 1, pos[1])
            else:
                rock.settle(pos, board)
                settled = True
            wind += 1
            if wind >= len(moves):
                wind = 0
        if pos[0] > top_idx:
            top_idx = pos[0]
    return top_idx + 1


lines = []
for line in sys.stdin:
    lines.append(line.strip())

moves = [*lines[0]]
board = [["."] * 7]
shapes = [Block(4, 1, {(0, 0), (0, 1), (0, 2), (0, 3)}),
          Block(3, 3, {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)}),
          Block(3, 3, {(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)}),
          Block(1, 4, {(0, 0), (1, 0), (2, 0), (3, 0)}),
          Block(2, 2, {(0, 0), (0, 1), (1, 0), (1, 1)})
          ]
print("part1:", simulate_tetris(-1, 0, shapes, moves, board, range(0, 2022)))

# after some empirical pattern occurrence matching, found a cycle in the tetris tower
CYCLE_TOWER_HEIGHT = 2738
CYCLE_LEN = 1720

cycle_begin = 1000000000000 - (1000000000000 // CYCLE_LEN) * CYCLE_LEN
total_cycles = (1000000000000 - cycle_begin) // CYCLE_LEN
board = [["."] * 7]

remainder = simulate_tetris(-1, 0, shapes, moves, board, range(0, cycle_begin))
print("part2:", CYCLE_TOWER_HEIGHT * total_cycles + remainder)
