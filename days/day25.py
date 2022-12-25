def parse(inp):
    return inp.splitlines()


def decode(n):
    out = 0
    for d in n:
        out *= 5
        match d:
            case '2':
                out += 2
            case '1':
                out += 1
            case '-':
                out -= 1
            case '=':
                out -= 2
    return out


def encode(n):
    out = []
    while n:
        d = n % 5
        match d:
            case 0:
                out.append('0')
            case 1:
                out.append('1')
            case 2:
                out.append('2')
            case 3:
                out.append('=')
                n += 2
            case 4:
                out.append('-')
                n += 1
        n //= 5
    return ''.join(reversed(out))



def part1(numbers):
    s = sum(map(decode, numbers))
    return encode(s)
