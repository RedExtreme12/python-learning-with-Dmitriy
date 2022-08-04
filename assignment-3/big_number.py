import re
from itertools import islice, chain


def index(string: str, needle_numbers: tuple[int, ...] | int, k: int = 5) -> tuple[int | list[int, ...]]:
    if isinstance(needle_numbers, int):
        needle_numbers = (needle_numbers, )

    total_occurrences = 0
    finded_indexes = {}

    for needle_number in needle_numbers:
        matches = [m.start() + 1 for m in re.finditer(str(needle_number), string)]
        total_matched = len(matches)
        total_occurrences += total_matched
        finded_indexes[needle_number] = matches[:k]

    needle_indexes = sorted([*chain.from_iterable(finded_indexes.values())])

    return total_occurrences, needle_indexes[:k]


if __name__ == '__main__':
    assert (1, [1]) == index('123', 1)
    assert (13, [1, 1, 2]) == index('1212122222', (1, 2, 12), 3)
