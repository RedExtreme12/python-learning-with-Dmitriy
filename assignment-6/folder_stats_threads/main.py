import concurrent
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from pprint import pprint

from folder_handler import FolderHandler
from thread_safe_dict import ThreadSafeDict


def calculate_stats(path: str):

    root_folder = Path(path)
    if not root_folder.exists() or not root_folder.is_dir():
        raise NotADirectoryError('Path does not exists or this is not a directory')

    ts_dict = ThreadSafeDict()
    futures = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        fh = FolderHandler(root_folder, executor, ts_dict, futures)
        init_future = executor.submit(fh)
        futures.append(init_future)

        for future in concurrent.futures.as_completed(futures):
            future.result()

    return ts_dict


pprint(calculate_stats('/Users/dzmitryrahozenka/PycharmProjects/Learning/python-learning-with-Dmitriy/assignment-6/'
                       'root_folder'))
