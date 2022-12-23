import re
import math
import collections


def parse(inp):
    tiles, instrs = inp.split('\n\n')
    tiles = tiles.splitlines()

    n_tiles = sum(t != ' ' for row in tiles for t in row)
    size = round(math.pow(n_tiles // 6, 0.5))
    w = max(len(row) for row in tiles) // size
    h = len(tiles) // size

    start = None
    sides = dict()
    for sy in range(h):
        y = sy * size
        for sx in range(w):
            x = sx * size
            if x >= len(tiles[y]) or tiles[y][x] == ' ':
                continue
            if start is None:
                start = sx,sy
            side = [row[x:x+size] for row in tiles[y:y+size]]
            sides[sx, sy] = side

    instrs = re.findall(r'\d+|L|R', instrs)
    return start, sides, size, w, h, instrs


def move(pos, d):
    dirs = [(1,0), (0,1), (-1,0), (0,-1)]
    return tuple(a+b for a,b in zip(pos, dirs[d]))


def part1(board):
    start, sides, size, w, h, instrs = board

    # Figure out neighbors of each tile
    neighbors = collections.defaultdict(list)
    for side in sides:
        for d in range(4):
            nxt_side = side
            while True:
                nx, ny = move(nxt_side, d)
                nxt_side = nx % w, ny % h
                if nxt_side in sides:
                    break
                nxt_side = nx, ny
            neighbors[side].append(nxt_side)

    d = 0
    pos = 0,0
    side = start
    for instr in instrs:
        if instr == 'R':
            d = (d+1) % 4
        elif instr == 'L':
            d = (d-1) % 4
        else:
            for _ in range(int(instr)):
                nx, ny = move(pos, d)
                cx, nx = divmod(nx, size)
                cy, ny = divmod(ny, size)
                nxt_side = neighbors[side][d] if cx or cy else side

                if sides[nxt_side][ny][nx] == '#':
                    break
                pos = nx, ny
                side = nxt_side

    x = side[0]*size + pos[0] + 1
    y = side[1]*size + pos[1] + 1
    return 1000*y + 4*x + d


