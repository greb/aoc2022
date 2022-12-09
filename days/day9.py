DIR = {'R': (1,0), 'U': (0,-1), 'L': (-1,0), 'D': (0,1)}

def parse(inp):
    moves = []
    for line in inp.splitlines():
        d, v = line.split()
        moves.append((d, int(v)))
    return moves


def move_knot(knot, d):
    return tuple(a+b for a,b in zip(knot, d))


def follow_knot(head, tail):
    dx, dy = (a-b for a,b in zip(head, tail))

    if abs(dx) > 1 or abs(dy) > 1:
        if abs(dx) > 1:
            dx = dx+1 if dx < 0 else dx-1
        if abs(dy) > 1:
            dy = dy+1 if dy < 0 else dy-1
        return move_knot(tail, (dx, dy))

    return tail


def move_rope(rope, move):
    visited = set()
    d, v = move
    for _ in range(v):
        new_rope = [move_knot(rope[0], DIR[d])]
        for knot in rope[1:]:
            knot = follow_knot(new_rope[-1], knot)
            new_rope.append(knot)
        rope = new_rope
        visited.add(rope[-1])
    return rope, visited


def solve(moves, n):
    visited = set()
    rope = [(0,0)] * n
    for move in moves:
        rope, v = move_rope(rope, move)
        visited.update(v)
    return len(visited)


def part1(moves):
    return solve(moves, 2)


def part2(moves):
    return solve(moves, 10)

