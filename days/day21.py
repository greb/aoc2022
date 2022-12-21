import re

HUMAN = 'humn'

def parse(inp):
    monkeys = {}

    const = re.compile(r'(\w+): (\d+)')
    calc = re.compile(r'(\w+): (\w+) (.) (\w+)')

    for line in inp.splitlines():
        if m := const.match(line):
            dst, val = m.groups()
            monkeys[dst] = int(val)

        elif m := calc.match(line):
            dst, *args = m.groups()
            monkeys[dst] = tuple(args)

    return monkeys


def eval_monkeys(monkeys, dst='root'):
    if isinstance(monkeys[dst], int):
        return monkeys[dst], dst == HUMAN

    monkey_a, op, monkey_b = monkeys[dst]
    val_a, hum_a = eval_monkeys(monkeys, monkey_a)
    val_b, hum_b = eval_monkeys(monkeys, monkey_b)

    match op:
        case '+': val = val_a + val_b
        case '-': val = val_a - val_b
        case '*': val = val_a * val_b
        case '/': val = val_a // val_b

    return val, hum_a or hum_b


def part1(monkeys):
    return eval_monkeys(monkeys)[0]


def ask_human(monkeys, dst='root', target=None):
    if dst == HUMAN:
        return target

    monkey_a, op, monkey_b = monkeys[dst]
    val_a, hum_a = eval_monkeys(monkeys, monkey_a)
    val_b, hum_b = eval_monkeys(monkeys, monkey_b)

    if hum_a:
        if dst == 'root':
            return ask_human(monkeys, monkey_a, val_b)

        match op:
            case '+': target = target - val_b
            case '-': target = target + val_b
            case '*': target = target // val_b
            case '/': target = target * val_b
        return ask_human(monkeys, monkey_a, target)

    elif hum_b:
        if dst == 'root':
            return ask_human(monkeys, monkey_b, val_a)

        match op:
            case '+': target = target - val_a
            case '-': target = val_a - target
            case '*': target = target // val_a
            case '/': target = val_a // target
        return ask_human(monkeys, monkey_b, target)

def part2(monkeys):
    return ask_human(monkeys)
