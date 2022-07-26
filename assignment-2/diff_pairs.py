from collections import Counter


def get_pairs_count(collection: list | tuple, m: int) -> int:
    converted_coll_set = set(collection)
    unique_pairs = set()
    amount_of_each_number = Counter(collection)

    for number in collection:
        abs_difference_for_estimated_pair = abs(number - m)

        if abs_difference_for_estimated_pair == number and amount_of_each_number[number] == 1:
            continue

        if abs_difference_for_estimated_pair in converted_coll_set:
            estimated_pair = (number, abs_difference_for_estimated_pair)

            if estimated_pair not in unique_pairs and tuple(reversed(estimated_pair)) not in unique_pairs:
                unique_pairs.add(estimated_pair)

    return len(unique_pairs)


if __name__ == '__main__':
    assert get_pairs_count([5, 4, 3, 2, 1], 1) == 4
    assert get_pairs_count([1, 3, 1, 5, 4], 0) == 1
