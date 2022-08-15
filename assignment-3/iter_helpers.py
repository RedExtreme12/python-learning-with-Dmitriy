from typing import Iterable


def transpose(matrix: Iterable[Iterable]) -> Iterable:
    return zip(*matrix)


def convert_str_to_int(x) -> int:
    if isinstance(x, str):
        return int(x, 0)
    return x


def scalar_product(iterable_1: Iterable, iterable_2: Iterable) -> int | None:
    try:
        return sum(map(lambda x, y: convert_str_to_int(x) * convert_str_to_int(y), iterable_1, iterable_2))
    except ValueError:
        return None
