import time


USE_CLASSIC_IMPLEMENTATION_OF_MERGE_FUNCTION = False


def merge(list_1: list | tuple, list_2: list | tuple) -> list | tuple:
    if USE_CLASSIC_IMPLEMENTATION_OF_MERGE_FUNCTION:
        return merge_classic(list_1, list_2)
    else:
        return merge_without_indexing(list_1, list_2)


def merge_classic(list_1: list | tuple, list_2: list | tuple) -> list | tuple:
    pointer_list_1, pointer_list_2 = 0, 0
    size_of_list_1, size_of_list_2 = len(list_1), len(list_2)

    result_list = []

    while pointer_list_1 <= (size_of_list_1 - 1) and pointer_list_2 <= (size_of_list_2 - 1):
        if list_1[pointer_list_1] <= list_2[pointer_list_2]:
            result_list.append(list_1[pointer_list_1])
            pointer_list_1 += 1
        else:
            result_list.append(list_2[pointer_list_2])
            pointer_list_2 += 1

    if pointer_list_1 <= size_of_list_1:
        result_list.extend(list_1[pointer_list_1: pointer_list_1 + 1])

    if pointer_list_2 <= size_of_list_2:
        result_list.extend(list_2[pointer_list_2: pointer_list_2 + 1])

    if type(list_1) is tuple or type(list_2) is tuple:
        return tuple(result_list)
    else:
        return result_list


def get_next_item(lst: list):
    try:
        next_item = lst.pop()
    except IndexError:
        next_item = None

    return next_item


def merge_without_indexing(list_1: list | tuple, list_2: list | tuple) -> list | tuple:
    result_list = []

    started_type_of_list_1 = type(list_1)
    started_type_of_list_2 = type(list_2)

    list_1 = list(list_1)
    list_2 = list(list_2)

    pointer_list_1, pointer_list_2 = list_1.pop(), list_2.pop()

    while True:
        if pointer_list_1 >= pointer_list_2:
            result_list.append(pointer_list_1)

            pointer_list_1 = get_next_item(list_1)
            if not pointer_list_1:
                break
        else:
            result_list.append(pointer_list_2)

            pointer_list_2 = get_next_item(list_2)
            if not pointer_list_2:
                break

    if pointer_list_1:
        result_list.append(pointer_list_1)
        result_list.extend(list_1)
    if pointer_list_2:
        result_list.append(pointer_list_2)
        result_list.extend(list_2)

    result_list = reversed(result_list)

    if started_type_of_list_1 is tuple or started_type_of_list_2 is tuple:
        return tuple(result_list)
    else:
        return list(result_list)


if __name__ == '__main__':
    a = [2, 8, 8]
    b = [3, 4, 5, 5, 10]

    merge(a, b)

    start = time.time()
    assert merge([1, 2, 7], [3]) == [1, 2, 3, 7]
    end = time.time()
    # print(end - start)

    start = time.time()
    assert merge((3, 15), (7, 8)) == (3, 7, 8, 15)
    end = time.time()
    # print(end - start)


