import re
import functools
import itertools
import collections

def parse(inp):
    valves = []
    rates = dict()
    graph = collections.defaultdict(lambda: 1000)

    pattern = re.compile(r'Valve (\w+) .*=(\d*); .* valves? (.*)')

    for line in inp.splitlines():
        valve, rate, tunnels = pattern.match(line).groups()
        valves.append(valve)
        if rate != '0':
            rates[valve] = int(rate)
        for edge in tunnels.split(', '):
            graph[(valve, edge)] = 1

    for a, b, c in itertools.product(valves, repeat=3):
        graph[b,c] = min(graph[b,c], graph[b,a] + graph[a,c])

    return rates, graph


def part1(valves):
    rates, graph = valves

    @functools.cache
    def search(time, curr='AA', closed=frozenset(rates)):
        scores = [0]
        for valve in closed:
            move_time = graph[curr, valve]
            if move_time >= time:
                continue
            new_time = time - move_time - 1
            score = rates[valve] * new_time
            score += search(new_time, valve, closed - {valve})
            scores.append(score)
        return max(scores)

    return search(30)


def part2(valves):
    rates, graph = valves

    @functools.cache
    def search(time, curr='AA', closed=frozenset(rates), e=False):
        scores = [search(26, closed=closed) if e else 0]
        for valve in closed:
            move_time = graph[curr, valve]
            if move_time >= time:
                continue
            new_time = time - move_time - 1
            score = rates[valve] * new_time
            score += search(new_time, valve, closed - {valve}, e)
            scores.append(score)
        return max(scores)

    return search(26, e=True)
