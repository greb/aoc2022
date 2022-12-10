WIDTH = 40
HEIGHT = 6

def parse(inp):
    cmds = iter(inp.splitlines())
    reg = 1
    addx_buf = None

    data = []
    for _ in range(WIDTH*HEIGHT):
        data.append(reg)

        if addx_buf:
            reg += addx_buf
            addx_buf = None
        else:
            cmd = next(cmds).split()
            if cmd[0] == 'addx':
                addx_buf = int(cmd[1])
    return data


def part1(data):
    signal = 0
    for c, reg in enumerate(data):
        if c % WIDTH == 19:
            signal += (c+1)*reg
    return signal


def part2(data):
    scan_line = []
    for c, reg in enumerate(data):
        x = c % WIDTH
        pix = '#' if abs(x-reg) <= 1 else '.'
        scan_line.append(pix)

        if x == WIDTH - 1:
            print(''.join(scan_line))
            scan_line = []
    return 'see output'

