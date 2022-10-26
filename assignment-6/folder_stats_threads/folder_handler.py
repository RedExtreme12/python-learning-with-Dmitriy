from utils import get_file_hash
from exceptions import StatNotCalculatedError

from dataclasses import dataclass
from collections import UserDict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import logging
import sys
import hashlib


handler = logging.StreamHandler(stream=sys.stdout)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


@dataclass
class FolderInfo:
    total_files: int
    total_size: int  # in bytes
    check_sum: str


class FolderHandler:

    def __init__(self,
                 source_folder: Path,
                 tp_executor: ThreadPoolExecutor,
                 storage_for_results: UserDict[str | FolderInfo] | dict[str | FolderInfo],
                 futures: list):
        self._storage = storage_for_results
        self._tp_executor = tp_executor
        self._source_folder = source_folder
        self._futures = futures

        self._traversed = True
        self._stat = FolderInfo(0, 0, '')

    @property
    def storage(self):
        return self._storage

    def _add_to_queue(self, file_: Path) -> None:
        fh = FolderHandler(file_, self._tp_executor, self._storage, self._futures)
        future = self._tp_executor.submit(fh)
        self._futures.append(future)
        self._traversed = False

        logger.debug(f'Folder {file_.name} added to Queue!')

    def _increase_stat(self, total_size: int = 0, total_files: int = 0, check_sum: str = '') -> None:
        self._stat.total_size += total_size
        self._stat.total_files += total_files
        self._stat.check_sum += check_sum

    def _get_checksums_of_dirs(self) -> str:
        result_hash = []

        for file_ in self._source_folder.iterdir():
            if file_.is_dir():
                abs_path_to_file = file_.absolute()

                folder_stat: FolderInfo = self._storage.get(abs_path_to_file, None)
                if not folder_stat:
                    raise StatNotCalculatedError(f'Stat for the {abs_path_to_file} folder have not yet been calculated')

                result_hash.append(folder_stat.check_sum)

        return ''.join(result_hash)

    def _normalize_checksum(self) -> None:
        self._stat.check_sum = hashlib.md5(self._stat.check_sum.encode()).hexdigest()

    def __call__(self):
        for file_ in self._source_folder.iterdir():
            abs_path_to_file = file_.absolute()
            processed_file: FolderInfo = self._storage.get(abs_path_to_file)

            if processed_file:
                self._increase_stat(processed_file.total_size,
                                    processed_file.total_files,
                                    processed_file.check_sum)
                continue

            if file_.is_dir():
                self._add_to_queue(file_)
            else:
                file_size = file_.stat().st_size
                check_sum = get_file_hash(file_)

                file_stat = FolderInfo(1, file_size, check_sum)
                self._increase_stat(file_stat.total_size,
                                    file_stat.total_files,
                                    file_stat.check_sum)
                self._storage[abs_path_to_file] = file_stat

        if not self._traversed:
            self._add_to_queue(self._source_folder)
        else:
            checksums = self._get_checksums_of_dirs()
            self._increase_stat(check_sum=checksums)
            self._normalize_checksum()

            logger.debug(f'Folder {self._source_folder.name} information has been added to the dictionary')
            self._storage[self._source_folder.absolute()] = self._stat
            logger.debug(f'Returning a result for {self._source_folder.name}')
