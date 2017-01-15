# https://www.hackerrank.com/challenges/coin-change


def mocked_raw_input(fpOrString):
    def set_raw_input_string(fpOrString):
        if type(fpOrString) is str:
            for line in fpOrString.split('\n'):
                yield line
        else:
            for line in open(fpOrString):
                yield line
    yield_func = set_raw_input_string(fpOrString)

    def next_func():
        return next(yield_func)
    return next_func


def get_min_coins(coins, value, z=0):
    # print '\t' * z, 'value', value
    retVal = []
    if value in coins:
        result = {value: 1}
        # print '\t' * z, 'value in coins', result
        if result not in retVal:
            retVal.append(result)
    for coin in coins:
        if value % coin == 0:
            result = {coin: value // coin}
            # print '\t' * z, 'found list', result
            if result not in retVal:
                retVal.append(result)
    for coin in coins:
        if value - coin >= min(coins):
            # print '\t' * z, 'recursing coin %s for value %s' % (coin, value -
            # coin)
            results = get_min_coins(coins, value - coin, z + 1)
            if results:
                for result in results:
                    result[coin] = result.get(coin, 0) + 1
                    if result not in retVal:
                        retVal.append(result)
    return retVal


# Mock out raw_input
s = '''4 3
1 2 3'''
raw_input = mocked_raw_input(s)

# Read the inputs
value, _ = map(int, raw_input().split())
coins = set(map(int, raw_input().split()))

print value, coins
results = get_min_coins(coins, value)
print len(results), results

# Mock out raw_input
s = '''10 4
2 5 3 6'''
raw_input = mocked_raw_input(s)

# Read the inputs
value, _ = map(int, raw_input().split())
coins = set(map(int, raw_input().split()))

print value, coins
results = get_min_coins(coins, value)
print len(results), results
