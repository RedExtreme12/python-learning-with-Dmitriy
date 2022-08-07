from typing import Iterable


def transpose(matrix: Iterable[Iterable]) -> Iterable:
    return zip(*matrix)


def convert_to_number_with_base(s, base) -> int | None:
    try:
        return int(s, base)
    except ValueError:
        return None


def to_binary(s: str):
    return convert_to_number_with_base(s, 2)


def to_decimal(s: str):
    return convert_to_number_with_base(s, 10)


def to_hexadecimal(s: str):
    return convert_to_number_with_base(s, 16)


def convert_str_to_int(x) -> int:
    if isinstance(x, str):
        converted_decimal = to_decimal(x)
        if converted_decimal:
            return converted_decimal

        converted_binary = to_binary(x)
        if converted_binary:
            return converted_binary

        converted_hexadecimal = to_hexadecimal(x)
        if converted_hexadecimal:
            return converted_hexadecimal
    return x


def scalar_product(iterable_1: Iterable, iterable_2: Iterable) -> int | None:
    try:
        return sum(map(lambda x, y: convert_str_to_int(x) * convert_str_to_int(y), iterable_1, iterable_2))
    except TypeError:
        return None
