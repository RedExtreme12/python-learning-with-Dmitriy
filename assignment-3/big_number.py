import re
import logging
import sys
from itertools import islice, chain


handler = logging.StreamHandler(stream=sys.stdout)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def index(string: str, needle_numbers: tuple[int, ...] | int, k: int = 5) -> tuple[int | list[int, ...]]:
    if isinstance(needle_numbers, int):
        needle_numbers = (needle_numbers, )

    total_occurrences = 0
    found_indices = {}

    for needle_number in needle_numbers:
        matches = [m.start() + 1 for m in re.finditer(str(needle_number), string)]
        total_matched = len(matches)
        total_occurrences += total_matched
        found_indices[needle_number] = matches[:k]

        if total_matched > k:
            logger.info(f'Number of occurrences of an element {needle_number} is {total_matched},'
                        f' but only {k} occurrences were taken')

    needle_indexes = sorted([*chain.from_iterable(found_indices.values())])

    return total_occurrences, needle_indexes[:k]


if __name__ == '__main__':
    assert (1, [1]) == index('123', 1)
    assert (13, [1, 1, 2]) == index('1212122222', (1, 2, 12), 3)
