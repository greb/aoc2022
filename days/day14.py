import itertools

def interpolate(start, end):
    x1, y1 = start
    x2, y2 = end

    if x1 == x2:
        for y in range(min(y1,y2), max(y1,y2)+1):
            yield x1, y

    elif y1 == y2:
        for x in range(min(x1,x2), max(x1,x2)+1):
            yield x, y1


def parse(inp):
    grid = dict()
    bottom = 0

    for line in inp.splitlines():
        coords = line.split(' -> ')
        coords = [tuple(int(c) for c in coord.split(',')) for coord in coords]

        for start, end in zip(coords, coords[1:]):
            for pos in interpolate(start, end):
                grid[pos] = '#'
                if pos[1] > bottom:
                    bottom = pos[1]

    return grid, bottom


def debug_grid(grid):
    xs = [p[0] for p in grid.keys()]
    x_bounds = min(xs), max(xs)+1
    ys = [p[1] for p in grid.keys()]
    y_bounds = min(ys), max(ys)+1

    for y in range(*y_bounds):
        row = []
        for x in range(*x_bounds):
            row.append(grid.get((x,y), '.'))
        print(''.join(row))
    print()


def part1(grid):
    grid, bottom = grid
    grid = grid.copy()

    src = (500, 0)
    cnt = 0

    x, y = src
    while y < bottom:
        for move in [(x, y+1), (x-1,y+1), (x+1,y+1)]:
            if move not in grid:
                x,y = move
                break
        else:
            cnt += 1
            grid[(x,y)] = 'o'
            x,y = src
    return cnt


def part2(grid):
    grid, bottom = grid

    src = (500, 0)
    cnt = 0

    x,y = src
    while True:
        if y == bottom + 1:
            cnt += 1
            grid[(x,y)] = 'o'
            x,y = src
            continue

        for move in [(x, y+1), (x-1,y+1), (x+1,y+1)]:
            if move not in grid:
                x,y = move
                break
        else:
            cnt += 1
            grid[(x,y)] = 'o'
            if (x,y) == src:
                break
            x,y = src

    return cnt

