import unittest

from iter_helpers import transpose, scalar_product


class TestTranspose(unittest.TestCase):

    def test_transpose(self):
        test_cases = [
            {
                'arguments': {'matrix': [[1, -1], [2, 3]]},
                'expected':  [[1, 2], [-1, 3]]
            }
        ]

        for test_case in test_cases:
            result = transpose(**test_case['arguments'])
            self.assertEqual(test_case['expected'], list(map(list, result)))


class TestScalarProduct(unittest.TestCase):

    def test_scalar_product(self):
        test_cases = [
            {
                'arguments': {
                   'iterable_1': [1, '2'],
                   'iterable_2': [-1, 1],
                },
                'expected': 1,
            },
            {
                'arguments': {
                   'iterable_1': [1, 'xyz'],
                   'iterable_2': [-1, 1],
                },
                'expected': None,
            }
        ]

        for test_case in test_cases:
            result = scalar_product(**test_case['arguments'])
            self.assertEqual(test_case['expected'], result)


if __name__ == '__main__':
    unittest.main()
