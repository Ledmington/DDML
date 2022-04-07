"""
Utility function that checks whether the given value is of type int.
If the given value is not int, it raises a TypeError.
This function can take an optional predicate.
If the given value does not match the given predicate, it raises a ValueError.
It returns the given value.
"""


def assert_int(value, predicate=None):
    if type(value) is not int:
        raise TypeError
    if predicate is not None and not predicate(value):
        raise ValueError
    return value
