import sys


def mark_h(forest, visible):
    for i in range(0, len(forest)):
        visible[i][0] = 1
        top = forest[i][0]
        for j in range(0, len(forest[i])):
            if forest[i][j] > top:
                visible[i][j] = 1
                top = forest[i][j]
        visible[i][-1] = 1
        top = forest[i][-1]
        for j in reversed(range(0, len(forest[i]))):
            if forest[i][j] > top:
                visible[i][j] = 1
                top = forest[i][j]


def mark_v(forest, visible):
    for i in range(0, len(forest[0])):
        visible[0][i] = 1
        top = forest[0][i]
        for j in range(0, len(forest)):
            if forest[j][i] > top:
                visible[j][i] = 1
                top = forest[j][i]
        visible[-1][i] = 1
        top = forest[-1][i]
        for j in reversed(range(0, len(forest))):
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

mark_h(forest, visible)
mark_v(forest, visible)
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
