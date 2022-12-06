def parse(inp):
    return inp.strip()

def part1(inp):
    for i in range(len(inp)):
        seg = inp[i:i+4]
        if len(set(seg)) == 4:
            break
    return i+4

def part2(inp):
    for i in range(len(inp)):
        seg = inp[i:i+14]
        if len(set(seg)) == 14:
            break
    return i+14
