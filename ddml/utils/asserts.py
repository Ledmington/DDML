"""
This module contains some useful functions to simplify the user input checking.
"""


def assert_int(value, predicate=None):
    """
    Utility function that checks whether a given value is an integer.
    It can also check if the given value satisfies an optionally given predicate.

    Args:
        value: the value to check
        predicate: the optional predicate

    Returns:
        the given value

    Raises:
        TypeError: if value is not int
        ValueError: if the predicate is specified and the value does not satisfy it
    """

    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError
    if predicate is not None and not predicate(value):
        raise ValueError
    return value
