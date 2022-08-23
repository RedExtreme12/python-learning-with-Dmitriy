def smart_function():
    count_of_call = getattr(smart_function, 'count_of_call', 0) + 1
    setattr(smart_function, 'count_of_call', count_of_call)
    return count_of_call


if __name__ == '__main__':
    for real_call_count in range(1, 5):
        assert smart_function() == real_call_count
