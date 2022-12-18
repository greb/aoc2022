def parse(inp):
    lines = inp.splitlines()
    return set(tuple(int(d) for d in line.split(',')) for line in lines)

def neighbors(cube):
    for d in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
        yield tuple(a+b for a,b in zip(cube, d))


def part1(cubes):
    area = 0
    for cube in cubes:
        n_touch = sum(n in cubes for n in neighbors(cube))
        area += 6 - n_touch
    return area


def debug_cubes(cubes, outside, bounds):
    for z in range(*bounds[2]):
        print(f'z={z}')
        for y in range(*bounds[1]):
            row = []
            for x in range(*bounds[0]):
                cube = x,y,z
                c = ' '
                if cube in cubes and cube in outside:
                    c = 'X'
                elif cube in cubes:
                    c = '█'
                elif cube in outside:
                    c = '░'
                row.append(c)
            print(''.join(row))
        print()


def find_outside(cubes, bounds):
    start = tuple(d[0] for d in bounds)

    outside = set()
    stack = [start]

    while stack:
        curr = stack.pop()
        outside.add(curr)

        for nxt in neighbors(curr):
            if nxt in outside:
                continue
            if not all(a <= x < b for x, (a,b) in zip(nxt, bounds)):
                continue
            if nxt in cubes:
                continue
            stack.append(nxt)
    return outside


def part2(cubes):
    # Expand bounds +1 so we'll found all nooks and cranies on the surface
    # Found during testing with debug_cubes
    bounds = [(min(d)-1, max(d)+2) for d in zip(*cubes)]
    outside = find_outside(cubes, bounds)

    area = 0
    for cube in cubes:
        n_touch = sum(n in outside for n in neighbors(cube))
        area += n_touch
    return area
