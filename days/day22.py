import re
import math
import collections
import dataclasses

DIRS = [(1,0), (0,1), (-1,0), (0,-1)]

def parse(inp):
    tiles, instrs = inp.split('\n\n')
    tiles = tiles.splitlines()

    n_tiles = sum(t != ' ' for row in tiles for t in row)
    size = round(math.pow(n_tiles // 6, 0.5))
    w = max(len(row) for row in tiles) // size
    h = len(tiles) // size

    faces = list()
    for fy in range(h):
        y = fy * size
        for fx in range(w):
            x = fx * size
            if x >= len(tiles[y]) or tiles[y][x] == ' ':
                continue
            face = [row[x:x+size] for row in tiles[y:y+size]]
            faces.append(((fx,fy), face))

    instrs = re.findall(r'\d+|L|R', instrs)
    return faces, size, w, h, instrs


def move(pos, d):
    return tuple(a+b for a,b in zip(pos, DIRS[d]))


def part1(board):
    faces, size, w, h, instrs = board
    start = faces[0][0]
    faces = dict(faces)

    # Figure out neighbors of each tile
    neighbors = collections.defaultdict(list)
    for face in faces:
        for d in range(4):
            nxt_face = face
            while True:
                nx, ny = move(nxt_face, d)
                nxt_face = nx % w, ny % h
                if nxt_face in faces:
                    break
                nxt_face = nx, ny
            neighbors[face].append(nxt_face)

    d = 0
    pos = 0,0
    face = start
    for instr in instrs:
        if instr == 'R':
            d = (d+1) % 4
        elif instr == 'L':
            d = (d-1) % 4
        else:
            for _ in range(int(instr)):
                nx, ny = move(pos, d)
                cx, nx = divmod(nx, size)
                cy, ny = divmod(ny, size)
                nxt_face = neighbors[face][d] if cx or cy else face

                if faces[nxt_face][ny][nx] == '#':
                    break
                pos = nx, ny
                face = nxt_face

    x = face[0]*size + pos[0] + 1
    y = face[1]*size + pos[1] + 1
    return 1000*y + 4*x + d


@dataclasses.dataclass(frozen=True)
class Vec3:
    x: int
    y: int
    z: int

    def __matmul__(self, other):
        return Vec3(
            self.y*other.z - self.z*other.y,
            self.z*other.x - self.x*other.z,
            self.x*other.y - self.y*other.x)

    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z


def wrap_cube(start, faces):
    norms = dict()
    uvs = dict()
    edges = collections.defaultdict(list)

    u = Vec3(1,0,0)
    v = Vec3(0,1,0)
    stack = []
    stack.append((start, (u, v)))

    while stack:
        face, uv = stack.pop()
        if face not in faces or face in uvs:
            continue
        u, v = uv
        norm = v@u
        norms[norm] = face
        uvs[face] = uv

        nxt_uvs = [(u@v, v), (u, u@v), (v@u, v), (u, v@u)]
        for rot_dir, nxt_uv in enumerate(nxt_uvs):
            nu, nv = nxt_uv
            edges[face].append(nv@nu)
            nxt_face = move(face, rot_dir)
            stack.append((nxt_face, nxt_uv))

    neighbors = collections.defaultdict(list)
    for face, (u, v) in uvs.items():
        ref_us = [u@v, u, v@u, u]
        for nxt_norm, ref_u in zip(edges[face], ref_us):
            nxt_face = norms[nxt_norm]
            nxt_u, _ = uvs[nxt_face]

            # not the most elegant way, but it works
            # alternative: project to 2d, then look up rotation in DIRS
            rot = 0
            while nxt_u != ref_u:
                ref_u = nxt_norm @ ref_u
                rot += 1

            neighbors[face].append((nxt_face, rot))
    return neighbors


def part2(board):
    faces, size, w, h, instrs = board
    start = faces[0][0]
    faces = dict(faces)

    neighbors = wrap_cube(start, faces)

    d = 0
    pos = 0,0
    face = start
    for instr in instrs:
        if instr == 'R':
            d = (d+1) % 4
        elif instr == 'L':
            d = (d-1) % 4
        else:
            for _ in range(int(instr)):
                nx, ny = move(pos, d)
                cx, nx = divmod(nx, size)
                cy, ny = divmod(ny, size)

                nxt_d = d
                nxt_face = face

                if cx or cy:
                    nxt_face, rot = neighbors[face][d]
                    nxt_d = (d+rot) % 4
                    match rot:
                        case 1: # 90 deg
                            nx, ny = size-ny-1, nx
                        case 2: # 180 deg
                            nx, ny = size-nx-1, size-ny-1
                        case 3: # 270 deg
                            nx, ny = ny, size-nx-1

                if faces[nxt_face][ny][nx] == '#':
                    break

                d = nxt_d
                pos = nx, ny
                face = nxt_face


    x = face[0]*size + pos[0] + 1
    y = face[1]*size + pos[1] + 1
    return 1000*y + 4*x + d

