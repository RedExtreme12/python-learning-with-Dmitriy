from collections import Counter


def get_pairs_count(collection: list | tuple, m: int) -> int:
    amount_of_each_number = Counter(collection)
    total_unique_pairs = 0

    for number in collection:
        abs_difference_for_estimated_pair = abs(number - m)

        if abs_difference_for_estimated_pair in amount_of_each_number:
            if abs_difference_for_estimated_pair == number and \
                    amount_of_each_number[abs_difference_for_estimated_pair] > 1:
                total_unique_pairs += 1
            elif abs_difference_for_estimated_pair != number:
                total_unique_pairs += 1
            amount_of_each_number[abs_difference_for_estimated_pair] = 0

    return int(total_unique_pairs)


if __name__ == '__main__':
    assert get_pairs_count([5, 4, 3, 2, 1], 1) == 4
    assert get_pairs_count([1, 3, 1, 5, 4], 0) == 1
    assert get_pairs_count([2, 2, 2, 2, 4, 4, 4], 1) == 0
