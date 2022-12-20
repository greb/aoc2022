class Node:
    def __init__(self, val, prv=None, nxt=None):
        self.val = val
        self.prv = val
        self.nxt = val


def parse(inp):
    return [int(line) for line in inp.splitlines()]


def debug_ring(ring):
    seq = []
    node = ring[0]
    while True:
        seq.append(node.val)
        node = node.nxt

        if node == ring[0]:
            break
    print(seq)


def solve(seq, key=1, n_mix=1):
    nodes = [Node(n*key) for n in seq]

    for a, b in zip(nodes, nodes[1:]):
        a.nxt = b
        b.prv = a
    nodes[-1].nxt = nodes[0]
    nodes[0].prv = nodes[-1]

    for _ in range(n_mix):
        for node in nodes:
            node.prv.nxt = node.nxt
            node.nxt.prv = node.prv
            left, right = node.prv, node.nxt

            move = node.val % (len(nodes)-1)
            for _ in range(move):
                left = left.nxt
                right = right.nxt

            left.nxt, node.prv = node, left
            right.prv, node.nxt = node, right

    for node in nodes:
        if node.val == 0:
            break

    score = 0
    for _ in range(3):
        for _ in range(1000):
            node = node.nxt
        score += node.val
    return score


def part1(seq):
    return solve(seq)


def part2(seq):
    key = 811589153
    return solve(seq, key, 10)


