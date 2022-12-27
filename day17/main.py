import sys
from collections import deque


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


def sweep(board, offset):
    for i in range(offset):
        board.popleft()


def update_min(min_per_col, row_idx, offset, board):
    for i in range(row_idx - 4, row_idx):
        row = board[i]
        for j in range(len(row)):
            if row[j] == "#" and i + offset < min_per_col[j]:
                min_per_col[j] = i + offset
    return min_per_col


lines = []
for line in sys.stdin:
    lines.append(line.strip())

moves = [*lines[0]]
board = deque([["."] * 7])
shapes = [Block(4, 1, {(0, 0), (0, 1), (0, 2), (0, 3)}),
          Block(3, 3, {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)}),
          Block(3, 3, {(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)}),
          Block(1, 4, {(0, 0), (1, 0), (2, 0), (3, 0)}),
          Block(2, 2, {(0, 0), (0, 1), (1, 0), (1, 1)})
          ]
top_idx = -1
wind = 0
p1_result = 0
offset = 0
min_per_col = [sys.maxsize] * 7

#for i in range(1000000000000):
for i in range(2022):
    rock = shapes[i % len(shapes)]
    settled = False
    new_row = top_idx + 3 + rock.height - offset
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
            min_per_col = update_min(min_per_col, pos[0], offset, board)
            if min(min_per_col) > offset:
                offset = min(min_per_col)
                sweep(board, offset)
            settled = True
        wind += 1
        if wind >= len(moves):
            wind = 0
    if pos[0] + offset > top_idx:
        top_idx = pos[0] + offset
    if i == 2021:
        p1_result = top_idx + 1
        print("part1:", p1_result)
print("part2:", top_idx + 1)
