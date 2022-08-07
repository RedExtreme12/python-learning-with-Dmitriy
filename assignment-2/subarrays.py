import itertools


def get_subarrays_count(list_for_search: list[int, ...], needle: int) -> int:
    total_list_sum = sum(list_for_search)
    partial_sums = list(itertools.accumulate(list_for_search[:]))
    list_for_search_length = len(list_for_search)
    total_count_of_unique_pairs = 0

    for i in range(list_for_search_length + 1):
        for j in range(i, list_for_search_length):
            if i != j:
                sum_of_slice = (total_list_sum - partial_sums[i]) - (total_list_sum - partial_sums[j])

                if sum_of_slice == needle:
                    total_count_of_unique_pairs += 1
            elif partial_sums[i] == needle:
                total_count_of_unique_pairs += 1

    return total_count_of_unique_pairs


if __name__ == '__main__':
    assert get_subarrays_count([0, 1, 0], 1) == 4
    assert get_subarrays_count([1, 1, 1], 2) == 2
    assert get_subarrays_count([1, 0, 1, 1], 2) == 3
