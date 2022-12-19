import re

def parse(inp):
    blueprints = []

    for line in inp.splitlines():
        n, *cost = map(int, re.findall(r'\d+', line))
        blueprints.append(cost)
    return blueprints


def solve(cost, time):
    c_ore, c_clay, c_obs0, c_obs1, c_geo0, c_geo1 = cost
    max_r_ore = max(c_ore, c_clay, c_obs0, c_geo0)

    best = 0
    start = (time, 0, 0, 0, 0, 1, 0, 0, 0)
    stack = [start]
    visited = set()

    while stack:
        state = stack.pop()
        t, ore, clay, obs, geo, r_ore, r_clay, r_obs, r_geo = state

        best = max(best, geo)
        if t==0:
            continue

        # Prunes the states that can't possible catch up to the best score.
        # Under optimal condiations we could add a geode cracker at every
        # step yielding a geometrical grow curve (in form of triangular
        # numbers). Even if, under those circumstance, it isn't possible to
        # beat the current best score until the time runs out we can abort
        # the search early.
        if geo + t*r_geo + ((t-1)*t // 2) <= best:
            continue

        # Don't produce more robots than necessary
        r_ore = min(r_ore, max_r_ore)
        r_clay = min(r_clay, c_obs1)
        r_obs = min(r_obs, c_geo1)

        # Throw away excess material to reduce amount of states
        ore = min(ore, t*max_r_ore - r_ore*(t-1))
        clay = min(clay, t*c_obs1 - r_clay*(t-1))
        obs = min(obs, t*c_geo1 - r_obs*(t-1))

        state = t, ore, clay, obs, geo, r_ore, r_clay, r_obs, r_geo
        if state in visited:
            continue
        visited.add(state)

        n_ore = ore + r_ore
        n_clay = clay + r_clay
        n_obs = obs + r_obs
        n_geo = geo + r_geo

        stack.append((t-1,
            n_ore, n_clay, n_obs, n_geo,
            r_ore, r_clay, r_obs, r_geo))

        if ore >= c_ore:
            stack.append((t-1,
                n_ore-c_ore, n_clay, n_obs, n_geo,
                r_ore+1, r_clay, r_obs, r_geo))

        if ore >= c_clay:
            stack.append((t-1,
                n_ore-c_clay, n_clay, n_obs, n_geo,
                r_ore, r_clay+1, r_obs, r_geo))

        if ore >= c_obs0 and clay >= c_obs1:
            stack.append((t-1,
                n_ore-c_obs0, n_clay-c_obs1, n_obs, n_geo,
                r_ore, r_clay, r_obs+1, r_geo))

        if ore >= c_geo0 and obs >= c_geo1:
            stack.append((t-1,
                n_ore-c_geo0, n_clay, n_obs-c_geo1, n_geo,
                r_ore, r_clay, r_obs, r_geo+1))

    return best


def part1(blueprints):
    score = 0
    time = 24
    for n, cost in enumerate(blueprints):
        best = solve(cost, time)
        score += (n+1) * best
    return score


def part2(blueprints):
    score = 1
    time = 32

    for cost in blueprints[:3]:
        score *= solve(cost, time)
    return score
