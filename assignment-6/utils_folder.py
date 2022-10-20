from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from threading import Lock
from typing import NamedTuple
from pathlib import Path


class FolderInfo(NamedTuple):
    total_files: int
    total_size: int  # in bytes
    check_sum: int


def calculate_stats(path: str):
    # Schema: <abs_path_to_file_or_folder>: <FolderInfo_obj>

    lock = Lock()
    dirs_stats_results = {}

    def process_folder(folder_obj: Path, thread_pool_executor: ThreadPoolExecutor):
        total_files_in_this_folder = 0
        total_size_this_folder = 0
        traversed = True

        for file in folder_obj.iterdir():
            abs_path_to_file = file.absolute()

            with lock:
                processed_file: FolderInfo = dirs_stats_results.get(abs_path_to_file, None)

            if processed_file:
                total_size_this_folder += processed_file.total_size
                total_files_in_this_folder += processed_file.total_files
                continue

            traversed = False
            if file.is_dir():
                thread_pool_executor.submit(process_folder, file, thread_pool_executor)
            else:
                file_size = file.stat().st_size
                with lock:
                    dirs_stats_results[abs_path_to_file] = FolderInfo(1, file_size, 0)  # file, third – hash

                total_files_in_this_folder += 1
                total_size_this_folder += file_size

        if not traversed:
            thread_pool_executor.submit(process_folder, folder_obj, thread_pool_executor)
        else:
            result_info = FolderInfo(total_files_in_this_folder, total_size_this_folder, 0)
            with lock:
                dirs_stats_results[folder_obj.absolute()] = result_info

    root_folder = Path(path)
    if not root_folder.exists() or not root_folder.is_dir():
        raise NotADirectoryError('Path does not exists or this is not a directory')

    # folders processing
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(process_folder, root_folder, executor).result()

    pprint(dirs_stats_results)
    return dirs_stats_results[path]


print(calculate_stats('/Users/dzmitryrahozenka/PycharmProjects/Learning/python-learning-with-Dmitriy/assignment-6/'
                      'root_folder'))
