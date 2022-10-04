from timeit import default_timer
from functools import wraps


def profile(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = default_timer()
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = default_timer()
            print('Time of execution: ', end_time - start_time)

        return result
    return wrapper


@profile
def some_function():
    sum(range(1000))
    return 10


class timer:

    def __enter__(self):
        self.start_time = default_timer()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(default_timer() - self.start_time)


if __name__ == '__main__':
    some_function()
