import unittest
import random

from error_handling_decorator import handle_error


class TestErrorHandler(unittest.TestCase):

    def test_re_raise(self):
        @handle_error(re_raise=True)
        def some_function():
            x = 1 / 0

        self.assertRaises(ZeroDivisionError, some_function)

    def test_exc_type(self):
        @handle_error(re_raise=False, exc_type=KeyError)
        def some_function():
            x = 1 / 0

        self.assertRaises(ZeroDivisionError, some_function)


if __name__ == '__main__':
    unittest.main()
