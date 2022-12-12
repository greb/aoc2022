import heapq

DIR = [(1,0), (0,1), (-1,0), (0,-1)]

def parse(inp):
    grid = []

    for y, line in enumerate(inp.splitlines()):
        row = []
        for x, tile in enumerate(line):
            match tile:
                case 'S':
                    tile = 'a'
                    start = (x,y)
                case 'E':
                    tile = 'z'
                    end = (x,y)
            elevation = ord(tile) - ord('a')
            row.append(elevation)
        grid.append(row)
    return start, end, grid


def neighbors(node, dims):
    w, h = dims
    for d in DIR:
        new_node = tuple(a+b for a,b in zip(node, d))
        x, y = new_node
        if 0 <= x < w and 0 <= y < h:
            yield new_node


def get_elevation(node, grid):
    x, y = node
    return grid[y][x]


def shortest_path(start, end, grid):
    dims = len(grid[0]), len(grid)

    dists = {start: 0}
    queue = [(0, start)]

    while queue:
        dist, node = heapq.heappop(queue)
        if node == end:
            return dist

        evel = get_elevation(node, grid)
        for neigh in neighbors(node, dims):
            neigh_evel = get_elevation(neigh, grid)
            if neigh_evel > evel+1:
                continue

            new_dist = dist + 1
            old_dist = dists.get(neigh)
            if not old_dist or new_dist < old_dist:
                dists[neigh] = new_dist
                heapq.heappush(queue, (new_dist, neigh))


def part1(inp):
    start, end, grid = inp
    return shortest_path(start, end, grid)


def part2(inp):
    _, end, grid = inp

    paths = []
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile == 0:
                start = (x,y)
                path = shortest_path(start, end, grid)
                if path:
                    paths.append(path)

    return min(paths)
