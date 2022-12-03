import itertools

def chunk_iter(it, n):
    it = iter(it)
    iters = [it] * n
    return zip(*iters)
