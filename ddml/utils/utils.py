def assert_int(value):
    if type(value) is not int:
        raise TypeError
    return value


def assert_int_pred(value, predicate):
    assert_int(value)
    if not predicate(value):
        raise ValueError
    return value
