import itertools


def unique(iterable):
    unique_elements_from_iterable = set(iterable)
    for unique_element in unique_elements_from_iterable:
        yield unique_element


if __name__ == '__main__':
    expected = [1, 2, 3]
    actual = unique([1, 2, 1, 3, 2])
    assert expected == list(actual)
