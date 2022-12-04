import re

def parse(inp):
    pattern = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')
    sections = []
    for line in inp.splitlines():
        section = pattern.match(line).groups()
        section = tuple(map(int, section))
        sections.append(section)
    return sections

def part1(sections):
    cnt = 0
    for a,b,c,d in sections:
        cnt += a >= c and b <= d or c >= a and d <= b
    return cnt


def part2(sections):
    cnt = 0
    for a,b,c,d in sections:
        cnt += a <= d and c <= b
    return cnt
