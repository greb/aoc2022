import unittest

from itertools import zip_longest
from functools import cmp_to_key

class TestParse(unittest.TestCase):
    def test_parse_expr(self):
        tests = [('[]', []),
                 ('[[[]]]', [[[]]]),
                 ('[1,2,3]', [1,2,3]),
                 ('[1[],[2,3,4]]', [[1],[2,3,4]]),
                 ('[[10,9],[9,10]]', [[10,9],[9,10]])]

        for expr, target in tests:
            out = parse_expr(expr)
            self.assertEqual(out, target)


def parse(inp):
    pairs = []
    for chunk in inp.split('\n\n'):
        lines = chunk.split('\n')
        a = parse_expr(lines[0])
        b = parse_expr(lines[1])
        pairs.append((a,b))
    return pairs


def parse_expr(expr):
    stack = []
    acc = None
    for c in expr:
        match c:
            case '[':
                stack.append(c)
            case ']':
                if acc is not None:
                    stack.append(acc)
                    acc = None
                lst = []
                while (item := stack.pop()) != '[':
                    lst.append(item)
                lst.reverse()
                stack.append(lst)
            case ',':
                if acc is not None:
                   stack.append(acc)
                   acc = None
            case _:
                if acc is None:
                    acc = int(c)
                else:
                    acc = acc*10 + int(c)
    return stack.pop()


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return left - right

    if isinstance(left, list) and isinstance(right, list):
        for l, r in zip_longest(left, right, fillvalue=None):
            if l is None:
                return -1
            if r is None:
                return 1
            cmp = compare(l, r)
            if cmp != 0:
                return cmp
        return 0

    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    return compare(left, right)


def part1(pairs):
    indices = 0
    for p, (left, right) in enumerate(pairs):
        if compare(left, right) < 0:
            indices += (p+1)
    return indices


def part2(pairs):
    dividers = ([[2]], [[6]])

    packets = []
    for p in pairs:
        packets.extend(p)
    packets.extend(dividers)

    packets = sorted(packets, key=cmp_to_key(compare))
    a = packets.index(dividers[0]) + 1
    b = packets.index(dividers[1]) + 1
    return a*b
