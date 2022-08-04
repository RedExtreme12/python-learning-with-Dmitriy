from typing import Iterable


def transpose(matrix: Iterable[Iterable]):
    return zip(*matrix)


def scalar_product(iterable_1: Iterable, iterable_2: Iterable) -> int | None:
    try:
        return sum(map(lambda x, y: float(x) * float(y), iterable_1, iterable_2))
    except ValueError:
        return None
