from copy import deepcopy


def merge_json(*dicts):
    immutable_types = (int, float, bool, str, frozenset, tuple)
    result_dict: dict = deepcopy(dicts[0])

    for _dict in dicts[1:]:
        for key, value in _dict.items():
            result_dict_value = result_dict.get(key, None)

            if type(result_dict_value) is type(value):
                if isinstance(value, immutable_types) and isinstance(result_dict_value, immutable_types):
                    result_dict[key] = value
                elif isinstance(value, list) and isinstance(result_dict_value, list):
                    result_dict_value.extend(value)
                elif isinstance(value, dict) and isinstance(result_dict_value, dict):
                    result_dict[key] = merge_json(result_dict_value, value)
            else:
                result_dict[key] = value

    return result_dict


if __name__ == '__main__':
    lhs = {'s': True, 'x': [2, 3], 'y': {'a': 1, 'b': 2, 'c': [11]}}
    rhs = {'s': False, 'x': [3, 4], 'y': {'a': 3, 'c': [12]}}
    expected = {'s': False, 'x': [2, 3, 3, 4], 'y': {'a': 3, 'b': 2, 'c': [11, 12]}}
    assert expected == merge_json(lhs, rhs)
