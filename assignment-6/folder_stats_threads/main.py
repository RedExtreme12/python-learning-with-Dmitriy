from collecting_stats_threads import calculate_stats
import logger_conf


PATH_FOR_STAT = '/Users/dzmitryrahozenka/Downloads/'


if __name__ == '__main__':
    result = calculate_stats(PATH_FOR_STAT)
    print(result)
