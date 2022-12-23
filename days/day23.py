import collections

def parse(inp):
    elves = set()
    for y, row in enumerate(inp.splitlines()):
        for x, tile in enumerate(row):
            if tile == '#':
                elves.add((x,y))
    return elves


ADJACENT = {
    'N': (0,-1), 'E': (1, 0), 'S': (0,1), 'W': (-1, 0),
    'NE': (1, -1), 'NW': (-1, -1), 'SE': (1, 1), 'SW': (-1, 1)
}

PROPOSE_EXCL = {
    'N': set(['N', 'NE', 'NW']),
    'S': set(['S', 'SE', 'SW']),
    'E': set(['E', 'NE', 'SE']),
    'W': set(['W', 'NW', 'SW'])
}


MOVES = {
    'N': (0,-1), 'E': (1, 0), 'S': (0,1), 'W': (-1, 0),
}

def adjacent(pos, elves):
    neighbors = set()
    for adj, move in ADJACENT.items():
        n_pos = tuple(p+m for p,m in zip(pos, move))
        if n_pos in elves:
            neighbors.add(adj)
    return neighbors


def round(elves, consider):
    prop_count = collections.defaultdict(int)
    prop_elves = dict()
    move_count = 0

    for elf in elves:
        neighbors = adjacent(elf, elves)
        if not neighbors:
            continue

        for c in consider:
            if neighbors & PROPOSE_EXCL[c]:
                continue

            nxt = tuple(p+m for p,m in zip(elf, MOVES[c]))
            prop_count[nxt] += 1
            prop_elves[elf] = nxt
            break

    new_elves = set()
    for elf in elves:
        nxt = prop_elves.get(elf)
        if nxt and prop_count[nxt] == 1:
            new_elves.add(nxt)
            move_count += 1
        else:
            new_elves.add(elf)

    consider.append(consider.popleft())
    return new_elves, move_count


def debug_elves(elves):
    xs, ys = zip(*elves)
    x_bound = min(xs), max(ys)+1
    y_bound = min(ys), max(ys)+1

    for y in range(*y_bound):
        row = []
        for x in range(*x_bound):
            tile = '#' if (x,y) in elves else '.'
            row.append(tile)
        print(''.join(row))
    print()


def part1(elves):
    consider = collections.deque('NSWE')

    for _ in range(10):
        elves, _ = round(elves, consider)

    xs, ys = zip(*elves)
    width = max(xs) - min(xs) + 1
    height = max(ys) - min(ys) + 1
    return width * height - len(elves)


def part2(elves):
    consider = collections.deque('NSWE')

    move_count = True
    round_count = 0
    while move_count:
        elves, move_count = round(elves, consider)
        round_count += 1

    return round_count
