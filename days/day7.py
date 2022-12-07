def parse(inp):
    stack = []
    sizes = []

    def up():
        size = stack.pop()
        sizes.append(size)
        if stack:
            stack[-1] += size

    for line in inp.splitlines():
        match line.split():
            case '$', 'cd', '..': up()
            case '$', 'cd', _: stack.append(0)
            case '$', _: pass
            case 'dir', _: pass
            case size, _: stack[-1] += int(size)

    while stack:
        up()

    return sizes


def part1(sizes):
    size_limit = 100_000
    return sum(s for s in sizes if s < size_limit)


def part2(sizes):
    min_size = max(sizes) - 40_000_000
    return min(s for s in sizes if s > min_size)


