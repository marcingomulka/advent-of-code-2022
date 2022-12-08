import sys


def mark_h(forest, visible, start, hrange):
    for i in range(len(forest)):
        visible[i][start] = 1
        top = forest[i][start]
        for j in hrange:
            if forest[i][j] > top:
                visible[i][j] = 1
                top = forest[i][j]


def mark_v(forest, visible, start, vrange):
    for i in range(len(forest[0])):
        visible[start][i] = 1
        top = forest[start][i]
        for j in vrange:
            if forest[j][i] > top:
                visible[j][i] = 1
                top = forest[j][i]


def score_h(value, curr, forest, range):
    score = 0
    for it in range:
        if forest[curr][it] < value:
            score += 1
        else:
            score += 1
            break
    return score


def score_v(value, curr, forest, range):
    score = 0
    for it in range:
        if forest[it][curr] < value:
            score += 1
        else:
            score += 1
            break
    return score


lines = []
for line in sys.stdin:
    lines.append(line.strip())

forest = []
visible = []
scores = []
for line in lines:
    forest.append(list(map(int, [*line])))
    visible.append([0] * len(line))
    scores.append([0] * len(line))

mark_h(forest, visible, 0, range(len(forest[0])))
mark_h(forest, visible, -1, range(len(forest[0]) - 1, 0, -1))
mark_v(forest, visible, 0, range(len(forest)))
mark_v(forest, visible, -1, range(len(forest) - 1, 0, -1))
print("part1: ", sum(map(sum, visible)))

row_count = len(forest)
for i in range(row_count):
    col_count = len(forest[i])
    for j in range(col_count):
        value = forest[i][j]
        scores[i][j] = score_h(value, i, forest, reversed(range(0, j))) \
                    * score_h(value, i, forest, range(j + 1, col_count)) \
                    * score_v(value, j, forest, reversed(range(0, i))) \
                    * score_v(value, j, forest, range(i + 1, row_count))
print("part2:", max(map(max, scores)))