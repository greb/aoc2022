import copy

def parse(inp):
    chunks = inp.split('\n\n')

    stacks = []
    for line in chunks[0].splitlines():
        crates = line[1::4]
        stacks.append(crates)

    stacks = [[c for c in crates[1:] if c != ' ']
               for crates in zip(*reversed(stacks))]

    moves = []
    for line in chunks[1].splitlines():
        w = line.split()
        m = int(w[1]), int(w[3])-1, int(w[5])-1
        moves.append(m)
    return stacks, moves


def part1(inp):
    stacks, moves = inp
    stacks = copy.deepcopy(stacks)
    for n, src, dst in moves:
        for _ in range(n):
            c = stacks[src].pop()
            stacks[dst].append(c)

    return ''.join(stack[-1] for stack in stacks)


def part2(inp):
    stacks, moves = inp

    for n, src, dst in moves:
        crates = stacks[src][-n:]
        del stacks[src][-n:]
        stacks[dst].extend(crates)

    return ''.join(stack[-1] for stack in stacks)


