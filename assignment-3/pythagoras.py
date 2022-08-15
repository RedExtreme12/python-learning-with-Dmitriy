import math


def get_pythagoras_triple(n: int) -> list[tuple[int, int, int], ...]:

    pythagoras_triple = [(x, y, z) for x in range(1, n + 1) for y in range(1, n + 1) for z in range(1, n + 1)
                         if z == math.sqrt(x ** 2 + y ** 2)]

    return pythagoras_triple


if __name__ == '__main__':
    get_pythagoras_triple(10)
