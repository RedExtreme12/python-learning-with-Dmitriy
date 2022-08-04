import math


def get_pythagoras_triple(n: int) -> list[tuple[int, int, int]]:

    pythagoras_triple = [(x, y, int(z)) for x in range(1, n) for y in range(1, n)
                         if (z := math.sqrt(x ** 2 + y ** 2)) % 1 == 0 and z <= n]

    return pythagoras_triple


if __name__ == '__main__':
    get_pythagoras_triple(10)
