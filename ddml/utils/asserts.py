def assert_int(value, predicate=None):
    """
    Utility function that checks whether a given value is an integer.
    It can also check if the given value satisfies an optionally given predicate.
    :param value: the value to check
    :param predicate: the optional predicate
    :return: the given value
    """
    if type(value) is not int:
        raise TypeError
    if predicate is not None and not predicate(value):
        raise ValueError
    return value
