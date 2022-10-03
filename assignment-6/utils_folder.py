import queue
from typing import NamedTuple
from pathlib import Path


class FolderInfo(NamedTuple):
    total_files: int
    total_size: int  # in bytes
    check_sum: int


def calculate_stats(path: str):
    p = Path(path)
    if not p.exists() or not p.is_dir():
        raise NotADirectoryError('Path does not exists or this is not a directory')

    total_files = 0
    queue_ = [p]

    while queue_:
        current_dir = queue_.pop(0)
        for file in current_dir.iterdir():
            total_files += 1
            if file.is_dir():
                queue_.append(file)

    return FolderInfo(total_files, p.stat().st_size, 0)


print(calculate_stats('/Users/dzmitryrahozenka/PycharmProjects/Learning/Django/djsite/coolsite/coolsite'))
