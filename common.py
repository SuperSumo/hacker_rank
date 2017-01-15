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
