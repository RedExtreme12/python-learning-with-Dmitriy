def get_primes(n: int) -> list:
    primes = [i for i in range(2, n + 1) if all(True if i % j != 0 else False for j in range(2, i))]
    return primes


if __name__ == '__main__':
    assert [2, 3, 5, 7, 11] == sorted(get_primes(11))
