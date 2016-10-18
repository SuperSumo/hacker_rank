# https://www.hackerrank.com/challenges/fibonacci-modified


def mocked_raw_input(fname):
    def set_raw_input_string(fname):
        for line in open(fname):
            yield line
    yield_func = set_raw_input_string(fname)

    def z():
        return next(yield_func)
    return z


# Mock out raw_input
open('input.txt', 'wt').write('2 2 20')
raw_input = mocked_raw_input('input.txt')

# Read the inputs
t0, t1, n = map(int, raw_input().split())
n -= 1


def memoize(f):
    cache = {}

    def memoizedFunction(args):
        if args not in cache:
            cache[args] = f(args)
        return cache[args]

    memoizedFunction.cache = cache
    return memoizedFunction


@memoize
def fib(n):
    if n == 0:
        return t0
    elif n == 1:
        return t1
    else:
        return fib(n - 2) + fib(n - 1)**2


print fib(n)
