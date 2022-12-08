import collections
directions = [
    (1, 0), (0, 1), (-1, 0), (0, -1)]

def parse(inp):
    return [[int(c) for c in row] for row in inp.splitlines()]


def part1(grid):
    visited = 0
    w, h = len(grid[0]), len(grid)

    for y, row in enumerate(grid):
        for x, tree in enumerate(row):
            for dx, dy in directions:
                trees = []

                tx = x+dx
                ty = y+dy
                while 0 <= tx < w and 0 <= ty < h:
                    trees.append(grid[ty][tx])
                    tx += dx
                    ty += dy

                if all(t < tree for t in trees):
                    visited += 1
                    break

    return visited


def part2(grid):
    best_score = 0
    w, h = len(grid[0]), len(grid)

    for y, row in enumerate(grid):
        for x, tree in enumerate(row):
            tree_score = 1

            for dx, dy in directions:
                dir_score = 0

                tx = x+dx
                ty = y+dy
                while 0 <= tx < w and 0 <= ty < h:
                    dir_score += 1
                    if grid[ty][tx] >= tree:
                        break
                    tx += dx
                    ty += dy

                tree_score *= dir_score

            if tree_score > best_score:
                best_score = tree_score

    return best_score
