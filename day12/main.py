import sys


def can_move(target, start):
    if start == "S":
        start = "a"
    if target == "E":
        target = "z"
    if ord(target) == ord(start) + 1 or ord(target) <= ord(start):
        return True


def get_neighbors(i, j, board):
    neighbors = []
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
    queue = [[start]]
    visited = {start}
    while len(queue) > 0:
        curr_path = queue.pop(0)
        last = curr_path[-1]
        neighbors = get_neighbors(last[0], last[1], board)
        if target in neighbors and can_move(board[target[0]][target[1]], board[last[0]][last[1]]):
            return len(curr_path)
        for neighbor in neighbors:
            if neighbor not in visited and can_move(board[neighbor[0]][neighbor[1]], board[last[0]][last[1]]):
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

