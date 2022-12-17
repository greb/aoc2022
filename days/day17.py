import itertools

rock_patterns = [
    ['####'],

    ['.#.',
     '###',
     '.#.'],

    ['..#',
     '..#',
     '###'],

    ['#',
     '#',
     '#',
     '#'],

    ['##',
     '##']
]

WIDTH = 7

rocks = []
for pattern in rock_patterns:
    rock = []
    for row in reversed(pattern):
        xs = [x+2 for x,r in enumerate(row) if r == '#']
        rock.append(set(xs))
    rocks.append(rock)


def parse(inp):
    return inp.strip()


def cave_collision(rock, rock_y, cave):
    for y, xs in enumerate(rock):
        y += rock_y
        if y >= len(cave):
            break
        if cave[y] & xs:
            return True

    return False


def push_rock(rock, push, rock_y, cave):
    d = 1 if push == '>' else -1
    new_rock = []
    for xs in rock:
        xs = [x+d for x in xs]
        if not all(0 <= x < WIDTH for x in xs):
            return rock
        new_rock.append(set(xs))

    if cave_collision(new_rock, rock_y, cave):
        return rock

    return new_rock


def drop_rock(cave, rock, pushes, push_idx):
    rock_y = len(cave) + 3

    while True:
        push = pushes[push_idx]
        push_idx = (push_idx+1) % len(pushes)

        rock = push_rock(rock, push, rock_y, cave)

        if rock_y == 0 or cave_collision(rock, rock_y-1, cave):
            break
        rock_y -= 1

    for y, xs in enumerate(rock):
        y += rock_y
        if y >= len(cave):
            cave.append(xs)
        else:
            cave[y] |= xs

    return push_idx


def part1(pushes):
    n = 2022

    cave = []
    push_idx = 0
    for idx in range(n):
        rock_idx = idx % len(rocks)
        rock = rocks[rock_idx]
        push_idx = drop_rock(cave, rock, pushes, push_idx)

    return len(cave)


def cave_profile(cave):
    unchecked = set(range(WIDTH))
    counts = [0]*WIDTH
    for row in reversed(cave):
        unchecked -= row
        for i in unchecked:
            counts[i] += 1
        if not unchecked:
            break

    return tuple(counts)


def part2(pushes):
    n = 1000000000000

    cave = []
    rock_idx = 0
    push_idx = 0
    idx = 0

    seen = dict()
    cycle_height = None

    while idx < n:
        rock_idx = idx % len(rocks)
        rock = rocks[rock_idx]
        push_idx = drop_rock(cave, rock, pushes, push_idx)

        if cycle_height is None:
            # profile doesn't detect overhangs, let's hope it works
            key = cave_profile(cave), rock_idx, push_idx
            if key in seen:
                s_height, s_idx = seen[key]
                d_height = len(cave) - s_height
                d_idx = idx - s_idx

                repeats = (n-idx) // d_idx
                cycle_height = repeats * d_height
                idx += repeats * d_idx
            else:
                seen[key] = len(cave), idx

        idx += 1

    return cycle_height + len(cave)

