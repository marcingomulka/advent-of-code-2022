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


def sweep(board, offset_end, offset_begin):
    print("sweep", offset_begin, offset_end)
    for i in range(offset_begin, offset_end):
        board.popleft()


def update_min(min_per_col, pos, offset, rock, board):
    row_idx = pos[0] - rock.height + 1
    # print("row_idx", row_idx)
    for j in range(pos[1], pos[1] + rock.width):
        if board[row_idx][j] == "#" and row_idx + offset > min_per_col[j]:
            # print("new min for col", j, "value=", row_idx + offset)
            min_per_col[j] = row_idx + offset
    return min_per_col


def print_board(board):
    for row in board:
        print("".join(row))


def calc_combinations(board):
    result = dict()
    for i in range(len(board) - 10):
        row = board[i]
        key = "".join(row)
        if key not in result.keys():
            result[key] = []
        result[key].append(i)
    return result


def diffs(values):
    first = values[0]
    result = []
    for i in range(1, len(values)):
        result.append(values[i] - first)
        first = values[i]
    return result


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
        key = ""
        if i > 10 and top_idx == 62:
            combs = calc_combinations(board)
            for key in combs.keys():
                occurs = combs[key]
                sorted(occurs)
                print(key, occurs)
                print(key, diffs(occurs))
                print(key, top_idx)
            print("????????????????????????????????????????")
    return top_idx+1


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
wind = 0
p1_result = simulate_tetris(-1, wind, shapes, moves, board, range(0, 2022))
print("part1:", p1_result)

# after some empirical pattern occurrence matching, found a cycle in the tetris tower
# cycle_len = 2738
# cycle_begin = 2821
cycle_len = 53
cycle_begin = 62
total_cycles = (1000000000000 - cycle_begin) // cycle_len
start = (1000000000000 - cycle_begin) % cycle_len
wind = start % len(moves)
board = [["."] * 7]

p2_result = simulate_tetris(0, shapes, moves, board, range(0, 20100))
#top = simulate_tetris(-1, 0, shapes, moves, board, range(0, cycle_begin + 3))
#print("total", total_cycles, "start", start, "top", top)
#print_board(board)
#board = board[cycle_begin:]
#print("????????????????????????")
#print_board(board)
#p2_result = simulate_tetris(top, wind, shapes, moves, board, range(3, start + 1))
#print(p2_result)
#print(cycle_len * total_cycles)
#print("part2:", p2_result + cycle_len * total_cycles)