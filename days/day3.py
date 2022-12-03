from . import utils

def parse(inp):
    return list(inp.splitlines())

def get_priority(item):
    if item.islower():
        return ord(item) - ord('a') + 1
    else:
        return ord(item) - ord('A') + 27


def part1(rucksacks):
    sum_priorities = 0

    for items in rucksacks:
        h = len(items) // 2
        in_both = set(items[:h]) & set(items[h:])
        assert len(in_both) == 1

        item = in_both.pop()
        sum_priorities += get_priority(item)

    return sum_priorities


def part2(rucksacks):
    sum_priorities = 0

    groups = utils.chunk_iter(rucksacks, 3)
    for group in groups:
        in_all = set(group[0]) & set(group[1]) & set(group[2])
        assert len(in_all) == 1

        item = in_all.pop()
        sum_priorities += get_priority(item)

    return sum_priorities
