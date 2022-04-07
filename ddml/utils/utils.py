def assert_int(value, predicate=None):
    if type(value) is not int:
        raise TypeError
    if predicate is not None and not predicate(value):
        raise ValueError
    return value
