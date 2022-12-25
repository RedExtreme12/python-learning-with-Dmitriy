import concurrent
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from folder_handler import FolderHandler
from thread_safe_containers.thread_safe_dict import ThreadSafeDict
from thread_safe_containers.thread_safe_set import ThreadSafeSet
import logger_conf


def calculate_stats(path: str):

    root_folder = Path(path)
    if not root_folder.exists() or not root_folder.is_dir():
        raise NotADirectoryError('Path does not exists or this is not a directory')

    ts_set_futures = ThreadSafeSet()
    ts_dict = ThreadSafeDict()
    with ThreadPoolExecutor(max_workers=2) as executor:
        fh = FolderHandler(root_folder, executor, ts_dict, ts_set_futures)
        init_future = executor.submit(fh)
        fh.current_future = init_future
        ts_set_futures.add(init_future)

        while ts_set_futures:
            concurrent.futures.wait(ts_set_futures, return_when=concurrent.futures.FIRST_COMPLETED)

    try:
        return ts_dict[root_folder]
    except KeyError:
        return None


PATH_FOR_STAT = '/Users/dzmitryrahozenka/Documents/Crypto'


if __name__ == '__main__':
    result = calculate_stats(PATH_FOR_STAT)
    print(result)
