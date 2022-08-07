def is_beauty(number: int) -> bool:
    return not ('0' in str(number) or number <= 0)


def get_beauties(k: int) -> tuple[int, int]:
    for i in range(k, -1, -1):
        diff = k - i
        if is_beauty(i) and is_beauty(diff):
            return diff, i


if __name__ == '__main__':
    assert get_beauties(13) == (1, 12)
    assert get_beauties(1010) == (11, 999)
    assert get_beauties(61) == (2, 59)
