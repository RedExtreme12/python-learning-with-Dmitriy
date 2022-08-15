import functools
import random
from typing import Any


class Memorize:

    ELEMENT_DELETED_MESSAGE = 'Elements has been deleted!'
    ELEMENT_ADDED_MESSAGE = 'Element has been added!'
    ELEMENT_RECEIVED_FROM_CACHE_MESSAGE = 'Element was fetched from the cache!'

    def __init__(self, maxsize: int | None = 128):
        self._arguments_with_results = {}
        self._max_size = maxsize
        self._total_elements = 0

    def __call__(self, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(kwargs.keys()), tuple(kwargs.values()))
            cached_result = self._arguments_with_results.get(key)

            if cached_result:
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

            print(self.ELEMENT_DELETED_MESSAGE)

    def _add_results_to_dict(self, key: tuple[tuple, tuple, tuple], value: Any) -> None:
        if self._max_size and self._total_elements == self._max_size:
            self._delete_randomly_element_from_dict(1)
            self._total_elements -= 1

        self._arguments_with_results[key] = value
        self._total_elements += 1

        print(self.ELEMENT_ADDED_MESSAGE)


class Convolve:

    def __init__(self, k: int):
        self._count_of_convolve = k

    def __call__(self, func):
        def wrapper(x):

            result = x
            for i in range(self._count_of_convolve):
                result = func(result)

            return result
        return wrapper


@Memorize(None)
def _sum(a, b, f, c=2):
    return a + b + f + c


@Memorize()
def calc(x, f):
    return x + f


@Convolve(3)
def f(some_argument):
    return 2 * some_argument


if __name__ == '__main__':
    x = 1
    assert f(x) == 2 * (2 * (2 * x))
