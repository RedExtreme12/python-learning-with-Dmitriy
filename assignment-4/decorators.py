import functools
import random
import sys
from typing import Any
import logging


handler = logging.StreamHandler(stream=sys.stdout)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class Memorize:
    ELEMENT_DELETED_MESSAGE = 'Elements has been deleted!'
    ELEMENT_ADDED_MESSAGE = 'Element has been added!'
    ELEMENT_RECEIVED_FROM_CACHE_MESSAGE = 'Element was fetched from the cache!'

    def __init__(self, maxsize: int | None = 128):
        self._arguments_with_results = {}
        self._max_size = maxsize

    def __call__(self, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(kwargs.keys()), tuple(kwargs.values()))
            cached_result = self._arguments_with_results.get(key)

            if cached_result:
                # logger.debug(self.ELEMENT_RECEIVED_FROM_CACHE_MESSAGE)
                print(self.ELEMENT_RECEIVED_FROM_CACHE_MESSAGE)
                return cached_result
            else:
                result = func(*args, **kwargs)
                self._add_results_to_dict(key, result)

                return result

        return wrapper

    def _delete_randomly_element_from_dict(self, count_of_elements_for_delete: int) -> None:
        for _ in range(count_of_elements_for_delete):
            self._arguments_with_results.pop(random.choice(tuple(self._arguments_with_results.keys())))

            # logger.debug(self.ELEMENT_DELETED_MESSAGE)
            print(self.ELEMENT_DELETED_MESSAGE)

    def _add_results_to_dict(self, key: tuple[tuple, tuple, tuple], value: Any) -> None:
        if self._max_size and len(self._arguments_with_results) == self._max_size:
            self._delete_randomly_element_from_dict(1)

        self._arguments_with_results[key] = value

        # logger.debug(self.ELEMENT_ADDED_MESSAGE)
        print(self.ELEMENT_ADDED_MESSAGE)


class Convolve:

    def __init__(self, k: int):
        self._count_of_convolve = k

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(x):
            result = x
            for i in range(self._count_of_convolve):
                result = func(result)

            return result

        return wrapper


def convolve(count_of_convolve: int):
    if not isinstance(count_of_convolve, int):
        raise TypeError('Argument count_of_convolve must have type int!')
    elif count_of_convolve < 1:
        raise ValueError('Argument count_of_convolve must be a natural number!')

    def inner(func):
        def wrapper(x):
            result = x
            for i in range(count_of_convolve):
                result = func(result)

            return result

        return wrapper

    return inner


@Memorize(None)
def _sum(a, b, f, c=2):
    return a + b + f + c


@Memorize()
def calc(x, f):
    return x + f


@convolve(3)
def f(some_argument):
    return 2 * some_argument


if __name__ == '__main__':
    x = 1
    assert f(x) == 2 * (2 * (2 * x))
    calc(10, 15)
    calc(10, 15)
    calc(10, 15)
    calc(20, 15)
