def distribute(selection, k):
    min_value = min(selection)
    max_value = max(selection)
    slc_weight = 1 / k

    hist = {i: 0 for i in range(k)}

    for selection_element in selection:
        if selection_element != max_value:
            slc = (selection_element - min_value) // ((max_value - min_value) * slc_weight)
        else:
            slc = k - 1
        hist[slc] += 1

    result = list(hist.values())

    return result


if __name__ == '__main__':
    assert distribute([1.25, 1, 2, 1.75], 2) == [2, 2]
