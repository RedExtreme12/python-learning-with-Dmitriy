import unittest
import io
from contextlib import redirect_stdout
from itertools import cycle, chain

from decorators import Memorize


class TestMemorize(unittest.TestCase):

    @staticmethod
    def _prepare_expected_stdout_string_only_new_elements(cache_size: int, count_of_elements: int) -> str:
        first_elements = '\n'.join((Memorize.ELEMENT_ADDED_MESSAGE for _ in range(cache_size)))
        cycler = cycle((Memorize.ELEMENT_DELETED_MESSAGE, Memorize.ELEMENT_ADDED_MESSAGE))
        other_elements = '\n'.join(next(cycler) for _ in range((count_of_elements - cache_size) * 2))

        return first_elements + '\n' + other_elements

    def test_memorize_of_func_with_positional_args(self):
        cache_size = 10

        @Memorize(cache_size)
        def _sum(a: int, b: int, c: int) -> int:
            return a + b + c

        out = io.StringIO()
        count_of_elements = 15
        args = ((i * 2, i * 4, i * 6) for i in range(count_of_elements))

        expected = self._prepare_expected_stdout_string_only_new_elements(cache_size, count_of_elements)

        with redirect_stdout(out):
            for arg in args:
                _sum(*arg)

        self.assertEqual(out.getvalue().rstrip('\n'), expected)

    def test_memorize_of_func_with_named_args(self):
        cache_size = 10

        @Memorize(cache_size)
        def _sum_kw_only(*, a: int, b: int, c: int) -> int:
            return a + b + c

        out = io.StringIO()
        args = ({'a': i, 'b': i + 1, 'c': i + 2} for i in range(3))
        args = chain(args, ({'a': 1, 'b': 2, 'c': 3}, ))

        expected = '\n'.join((Memorize.ELEMENT_ADDED_MESSAGE for _ in range(3))) + '\n'
        expected += Memorize.ELEMENT_RECEIVED_FROM_CACHE_MESSAGE

        with redirect_stdout(out):
            for arg in args:
                _sum_kw_only(**arg)

        self.assertEqual(out.getvalue().rstrip('\n'), expected)


if __name__ == '__main__':
    unittest.main()
