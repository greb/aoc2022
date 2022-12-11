import math
import re

def parse(inp):
    monkeys = []
    for chunk in inp.split('\n\n'):
        monkey = {}
        lines = chunk.splitlines()

        monkey['items'] =  [int(n) for n in re.findall(r'\d+', lines[1])]
        monkey['op'] = lines[2].split()[-2:]
        monkey['test'] = int(lines[3].split()[-1])
        monkey['cond'] = (
            int(lines[5].split()[-1]), # if_false
            int(lines[4].split()[-1])) # if_true

        monkeys.append(monkey)
    return monkeys


def operation(monkey, item):
    op, val = monkey['op']
    if val == 'old':
        return item*item
    elif op == '+':
        return item+int(val)
    else:
        return item*int(val)


def solve(monkeys, n, calm):
    cnt = [0]*len(monkeys)
    items = [m['items'].copy() for m in monkeys]

    for _ in range(n):
        for m, monkey in enumerate(monkeys):
            cnt[m] += len(items[m])
            for item in items[m]:
                item = operation(monkey, item)
                item = calm(item)
                cond = item % monkey['test'] == 0
                next = monkey['cond'][cond]
                items[next].append(item)
            items[m] = []

    a, b = list(sorted(cnt))[-2:]
    return a*b


def part1(monkeys):
    calm = lambda x: x // 3
    return solve(monkeys, 20, calm)


def part2(monkeys):
    correction = math.prod(m['test'] for m in monkeys)
    calm = lambda x: x % correction
    return solve(monkeys, 10_000, calm)

