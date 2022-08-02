import math


def get_primes(n: int) -> list:
    primes = [i for i in range(2, n + 1) if all(i % j != 0 for j in range(2, int(math.sqrt(i)) + 1))]
    return primes


if __name__ == '__main__':
    assert [2, 3, 5, 7, 11] == sorted(get_primes(11))
