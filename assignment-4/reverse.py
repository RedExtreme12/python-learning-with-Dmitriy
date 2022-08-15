from collections import defaultdict


def reverse_dict(_dict: dict):
    reversed_dict = defaultdict(list)

    for old_key, values in _dict.items():
        for value in values:
            reversed_dict[value].append(old_key)

    return dict(reversed_dict)


if __name__ == '__main__':
    initial = {2: [3, 5], 1: [1, 2], 5: [2]}
    assert reverse_dict(initial) == {3: [2], 5: [2], 1: [1], 2: [1, 5]}
    assert reverse_dict(initial) != {3: [2], 1: [1], 2: [1, 5]}
