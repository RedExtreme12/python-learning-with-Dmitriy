def add_to_intervals_set(valid_intervals: set, interval: list,
                         interval_indexes: tuple, sum_number: int) -> bool:
    if sum(interval) == sum_number:
        valid_intervals.add(interval_indexes)
        valid_intervals.add(tuple(reversed(interval_indexes)))
        return True
    return False


def get_subarrays_count(list_for_search: list, sum_number: int):
    lst = list_for_search[:]

    valid_intervals = set()
    total_valid_intervals = 0

    for i in range(len(lst)):

        for j in range(i, -1, -1):
            if (i, j) in valid_intervals:
                continue

            if i == j:
                estimated_interval = [lst[j]]
            elif j == 0:
                estimated_interval = lst[i:None:-1]
            else:
                estimated_interval = lst[i:j - 1:-1]

            estimated_interval_indexes = (i, j)
            if add_to_intervals_set(valid_intervals, estimated_interval, estimated_interval_indexes, sum_number):
                total_valid_intervals += 1
                break

        for j in range(i, len(lst)):
            if (i, j) in valid_intervals:
                continue

            estimated_interval = lst[i:j + 1:1]

            estimated_interval_indexes = (i, j)
            if add_to_intervals_set(valid_intervals, estimated_interval, estimated_interval_indexes, sum_number):
                total_valid_intervals += 1
                break

    return total_valid_intervals


if __name__ == '__main__':
    assert get_subarrays_count([0, 1, 0], 1) == 4
    assert get_subarrays_count([1, 1, 1], 2) == 2
    assert get_subarrays_count([1, 0, 1, 1], 2) == 3
