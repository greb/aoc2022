import re

from . import utils

def parse(inp):
    sensors = []
    for line in inp.splitlines():
        coords = [int(c) for c in re.findall(r'[xy]=(-?\d+)', line)]
        sensor = tuple(utils.chunk_iter(coords, 2))
        sensors.append(sensor)
    return sensors


def manhatten_dist(src, dst):
    return abs(src[0]-dst[0]) + abs(src[1]-dst[1])


def get_sections(sensors, y):
    sections = []
    for (sx,sy), (bx,by) in sensors:
        dist = manhatten_dist((sx,sy), (bx,by))
        dx = dist - abs(sy - y)
        if dx> 0:
            section = sx-dx, sx+dx
            sections.append(section)

    reduced = []
    for section in sorted(sections):
        if not reduced:
            reduced.append(section)
            continue

        last = reduced[-1]
        if section[0] <= last[1]:
            reduced[-1] = last[0], max(section[1], last[1])
        else:
            reduced.append(section)
    return reduced


def part1(sensors):
    y_target = 2_000_000
    overlap_beacons = set()
    for _, (bx,by) in sensors:
        if by == y_target:
            overlap_beacons.add(bx)

    cnt = 0
    for section in get_sections(sensors, y_target):
        cnt += section[1]-section[0]+1
    return cnt - len(overlap_beacons)


def part2(sensors):
    size = 4_000_000

    # It's slow, but it works
    for y in range(size):
        sections = get_sections(sensors, y)
        if len(sections) == 2:
            x = sections[0][1]+1
            return x*size + y
