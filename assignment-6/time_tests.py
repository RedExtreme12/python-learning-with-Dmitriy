from timeit import default_timer

from folder_stats_async import collecting_stats_async
from folder_stats_threads import collecting_stats_threads


PATH_FOR_STAT = '/Users/dzmitryrahozenka/Downloads/'


class timer:

    def __enter__(self):
        self.start_time = default_timer()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(default_timer() - self.start_time)


if __name__ == '__main__':

    print('------------')
    print('Async Version')
    print('------------')
    with timer():
        print(collecting_stats_async.get_summary_stat(PATH_FOR_STAT))

    print('------------')
    print('Threading Version')
    print('------------')
    with timer():
        print(collecting_stats_threads.calculate_stats(PATH_FOR_STAT))
