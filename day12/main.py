import sys
from collections import deque


def can_move(board, target, start):
    v_target = board[target[0]][target[1]]
    v_start = board[start[0]][start[1]]
    if v_start == "S":
        v_start = "a"
    if v_target == "E":
        v_target = "z"
    return ord(v_target) == ord(v_start) + 1 or ord(v_target) <= ord(v_start)


def get_neighbors(pos, board):
    neighbors = []
    i = pos[0]
    j = pos[1]
    if i - 1 >= 0:
        neighbors.append((i - 1, j))
    if i + 1 < len(board):
        neighbors.append((i + 1, j))
    if j - 1 >= 0:
        neighbors.append((i, j - 1))
    if j + 1 < len(board[i]):
        neighbors.append((i, j + 1))
    return neighbors


def bfs(start, target, board):
    queue = deque()
    visited = {start}
    queue.append([start])
    while len(queue) > 0:
        curr_path = queue.popleft()
        last = curr_path[-1]
        neighbors_list = get_neighbors(last, board)
        for neighbor in neighbors_list:
            if neighbor not in visited and can_move(board, neighbor, last):
                if target == neighbor:
                    return len(curr_path)
                new_path = curr_path.copy()
                new_path.append(neighbor)
                queue.append(new_path)
                visited.add(neighbor)
    return sys.maxsize


lines = []
for line in sys.stdin:
    lines.append(line.strip())

board = []
s_pos = (0, 0)
e_pos = (0, 0)
list_of_a = []
i = 0
for line in lines:
    row = [*line]
    for j in range(len(row)):
        if row[j] == "S":
            s_pos = (i, j)
        elif row[j] == "E":
            e_pos = (i, j)
        elif row[j] == "a":
            list_of_a.append((i, j))
    board.append(row)
    i += 1

print("part1:", bfs(s_pos, e_pos, board))

min_len = sys.maxsize
for a_pos in list_of_a:
    shortest = bfs(a_pos, e_pos, board)
    if shortest < min_len:
        min_len = shortest
print("part2:", min_len)

