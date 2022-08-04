from collections.abc import Iterable
from itertools import chain


def flatten(iterables):

    iterator = iter(iterables)

    while True:
        try:
            current = next(iterator)

            if isinstance(current, Iterable) and not isinstance(current, str):
                iterator = chain(current, iterator)
            else:
                yield current
        except StopIteration:
            break


if __name__ == '__main__':
    expected = [1, 2, 0, 1, 1, 2, 1, 'ab']
    actual = flatten(([1, 2, range(2), [[], [1], [[2]]], (x for x in [1]), 'ab']))
    assert expected == list(actual)

