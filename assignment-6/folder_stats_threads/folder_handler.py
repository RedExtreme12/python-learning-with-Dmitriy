from .utils import get_file_hash
from .exceptions import StatNotCalculatedError
from .thread_safe_containers.thread_safe_dict import ThreadSafeDict
from .thread_safe_containers.thread_safe_set import ThreadSafeSet
from .handle_error_context import HandleErrorContext
from .folder_info import FolderInfo

from concurrent.futures import ThreadPoolExecutor, Future
from pathlib import Path
from functools import partial
import hashlib
import logging

logger = logging.getLogger(f'logger_conf.{__name__}')


class FolderHandler:

    def __init__(self,
                 source_folder: Path,
                 tp_executor: ThreadPoolExecutor,
                 results_storage: ThreadSafeDict,
                 futures_storage: ThreadSafeSet,
                 current_future: Future = None):
        self._storage = results_storage
        self._tp_executor = tp_executor
        self._source_folder = source_folder

        self._futures = futures_storage
        self._current_future = current_future

        self._traversed = True
        self._stat = FolderInfo(0, 0, '')

    @property
    def storage(self) -> ThreadSafeDict:
        return self._storage

    @property
    def current_future(self) -> Future | None:
        return self._current_future

    @current_future.setter
    def current_future(self, future: Future) -> None:
        self._current_future = future

    @property
    def futures(self) -> ThreadSafeSet:
        return self._futures

    def _wait_until_current_future_is_not_set(self) -> None:
        """
        Waits until the option current_future is set. It is used because the initial future can start
        executing without this parameter, which in turn can lead to errors.
        :return: None
        """
        while not self.current_future:
            pass

    def _add_to_queue(self, file_: Path) -> None:
        fh = FolderHandler(file_, self._tp_executor, self.storage, self.futures)
        future = self._tp_executor.submit(fh)
        fh.current_future = future

        self.futures.add(future)
        self._traversed = False

        logger.debug(f'Folder {file_.name} added to Queue!')

    def _remove_from_queue(self, future: Future) -> None:
        self.futures.remove(future)

        logger.debug(f'The folder {self._source_folder.absolute()} has been removed from the queue!')

    def _increase_stat(self, total_size: int = 0, total_files: int = 0, check_sum: str = '') -> None:
        self._stat.total_size += total_size
        self._stat.total_files += total_files
        self._stat.check_sum += check_sum

    def _get_checksums_of_dirs(self) -> str:
        result_hash = []

        for file_ in self._source_folder.iterdir():
            if file_.is_dir():
                abs_path_to_file = file_.absolute()

                folder_stat: FolderInfo = self.storage.get(abs_path_to_file)
                if not folder_stat:
                    raise StatNotCalculatedError(f'Stat for {abs_path_to_file} folder have not yet been calculated')

                result_hash.append(folder_stat.check_sum)

        root_folder_hash_of_name = hashlib.md5(self._source_folder.name.encode()).hexdigest()
        result_hash.append(root_folder_hash_of_name)

        return ''.join(result_hash)

    def _normalize_checksum(self) -> None:
        self._stat.check_sum = hashlib.md5(self._stat.check_sum.encode()).hexdigest()

    def _traverse_folder(self) -> None:
        for file_ in self._source_folder.iterdir():

            abs_path_to_file = file_.absolute()
            processed_file: FolderInfo = self.storage.get(abs_path_to_file)

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
                self.storage[abs_path_to_file] = file_stat

    def __call__(self):
        self._wait_until_current_future_is_not_set()

        callback = partial(self._remove_from_queue, future=self.current_future)

        with HandleErrorContext(re_raise=False, log_traceback=True, exc_callback=callback):
            self._traverse_folder()

            if not self._traversed:
                self._add_to_queue(self._source_folder)
                self._remove_from_queue(self.current_future)
            else:
                checksums = self._get_checksums_of_dirs()
                self._increase_stat(check_sum=checksums)

                self._normalize_checksum()

                self._storage[self._source_folder.absolute()] = self._stat
                self._remove_from_queue(self.current_future)
