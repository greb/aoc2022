def parse(inp):
    calories = []

    cal = 0
    for line in inp.splitlines():
        if not line:
            calories.append(cal)
            cal = 0
        else:
            cal += int(line)
    calories.append(cal)
    return calories


def part1(calories):
    return max(calories)


def part2(calories):
    calories = list(sorted(calories))
    return sum(calories[-3:])

