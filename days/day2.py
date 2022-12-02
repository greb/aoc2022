def parse(inp):
    strat = []
    for line in inp.splitlines():
        a, b = line.split()
        a = ord(a) - ord('A')
        b = ord(b) - ord('X')
        strat.append((a,b))
    return strat

def part1(strat):
    score = 0

    for a, b in strat:
        score += b+1
        score += ((b+1 - a) % 3) * 3
    return score


def part2(strat):
    score = 0

    for a, b in strat:
        score += b*3
        score += ((a+b+2) % 3) + 1
    return score
