import collections

DIRS = {'>': (1, 0), 'v': (0, 1), '<': (-1,0), '^': (0, -1)}

class BlizzardCache:
    def __init__(self, objs, w, h):
        self.cache = [(objs, BlizzardCache.occupied(objs))]
        self.w = w
        self.h = h

        while True:
            objs = self.simulate(objs)
            if objs == self.cache[0][0]:
                break
            occ = BlizzardCache.occupied(objs)
            self.cache.append((objs, occ))


    @staticmethod
    def occupied(objs):
        occ = collections.defaultdict(int)
        for _, pos in objs:
            occ[pos] += 1
        return occ


    def simulate(self, objs):
        new_objs = []

        for mdir, pos in objs:
            x, y = tuple(p+d for p,d in zip(pos, DIRS[mdir]))
            x = ((x-1) % (self.w-2)) + 1
            y = ((y-1) % (self.h-2)) + 1
            new_objs.append((mdir, (x,y)))
        return new_objs

    def get(self, idx):
        idx = idx % len(self.cache)
        return self.cache[idx]


def parse(inp):
    grid = inp.splitlines()

    w, h = len(grid[0]), len(grid)
    start, end = None, None

    objs = []
    walls = set()
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            pos = x,y
            if tile == '.':
                if y == 0: start = pos
                elif y == h-1: end = pos
            elif tile in DIRS:
                objs.append((tile, pos))

    cache = BlizzardCache(objs, w, h)
    return start, end, w, h, cache


def shortes_path(start, end, w, h, cache, n_steps=0):
    queue = collections.deque([(n_steps, start)])
    visited = set()
    while queue:
        n_steps, pos = queue.popleft()

        if (n_steps, pos) in visited:
            continue
        visited.add((n_steps, pos))

        n_steps += 1
        _, occupied = cache.get(n_steps)

        for ndir in DIRS.values():
            nxt_pos = tuple(p+d for p,d in zip(pos, ndir))
            if nxt_pos == end:
                return n_steps

            x, y = nxt_pos
            if x < 1 or x >= w-1 or y < 1 or y >= h-1:
                continue
            if nxt_pos in occupied:
                continue
            queue.append((n_steps, nxt_pos))

        if pos not in occupied:
            queue.append((n_steps, pos)) # wait


def part1(grid):
    start, end, w, h, cache = grid
    return shortes_path(start, end, w, h, cache)


def part2(grid):
    start, end, w, h, cache = grid

    a = shortes_path(start, end, w, h, cache)
    b = shortes_path(end, start, w, h, cache, a)
    c = shortes_path(start, end, w, h, cache, b)
    return c

