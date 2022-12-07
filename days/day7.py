def parse(inp):
    # First two lines are always the same
    lines = iter(inp.splitlines()[2:])

    dir_sizes = []
    total_size = parse_dirs(lines, dir_sizes)
    return total_size, dir_sizes


def parse_dirs(it, dir_sizes):
    size = 0

    try:
        while True:
            tokens = next(it).split()
            if tokens[0] == '$':
                if tokens[1] == 'cd':
                    if tokens[2] == '..':
                        return size
                    else:
                        sub_size = parse_dirs(it, dir_sizes)
                        dir_sizes.append(sub_size)
                        size += sub_size
            elif tokens[0] != 'dir':
                size += int(tokens[0])

    except StopIteration:
        pass

    return size


def part1(sizes):
    _, dir_sizes = sizes
    size_limit = 100_000
    return sum(s for s in dir_sizes if s < size_limit)


def part2(sizes):
    total_size, dir_sizes = sizes
    min_size = total_size - 40_000_000
    return min(s for s in dir_sizes if s > min_size)


