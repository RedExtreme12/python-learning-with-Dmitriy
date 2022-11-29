from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
import asyncio
import hashlib
import logging
import sys
import os


handler = logging.StreamHandler(stream=sys.stdout)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


@dataclass
class FolderInfo:
    total_files: int
    total_size: int  # in bytes
    check_sum: str


async def get_file_size(file_: Path) -> int | None:
    try:
        return file_.stat().st_size
    except OSError as err:
        logger.debug(f'Unable to calculate size of file {file_.name}, because {err.strerror}')
        return None


async def get_file_checksum(file_: Path) -> str | None:
    checksum = hashlib.md5()

    try:
        with file_.open('rb') as file_cursor:
            while True:
                chunk = file_cursor.read(4096)
                if not chunk:
                    break
                checksum.update(chunk)
    except OSError as err:
        logger.debug(f'{file_.name} cannot be open, because {err.strerror}')
        return None
    else:
        checksum.update(file_.name.encode())
        return checksum.hexdigest()


def update_checksum(file_: Path, checksum_to_update, checksum_from_update: str):
    if checksum_from_update:
        checksum_to_update.update(checksum_from_update.encode())
        if file_.is_dir():
            checksum_to_update.update(file_.name.encode())


async def generate_folder_statistics(folder: Path, storage_stats: dict[Path, FolderInfo]) -> FolderInfo:
    total_files = 0
    total_size = 0
    checksum_folder = hashlib.md5()

    for file_obj in folder.iterdir():
        file_obj_stat = storage_stats.get(file_obj.absolute())

        if file_obj_stat:
            total_files += file_obj_stat.total_files
            total_size += file_obj_stat.total_size

            update_checksum(file_obj, checksum_folder, file_obj_stat.check_sum)

    folder_stat = FolderInfo(total_files, total_size, checksum_folder.hexdigest())
    return folder_stat


async def get_abs_name_of_file(file_: Path) -> Path | None:
    try:
        abs_path_to_file = file_.absolute()
    except OSError as err:
        logger.debug(f'{file_.name} cannot be calculated, because {err.strerror}')
        return None

    return abs_path_to_file


async def check_dir_is_available(file_: Path) -> bool:
    try:
        is_available = file_.is_dir() and os.access(file_, os.R_OK)
    except OSError as err:
        is_available = False

    return is_available


async def get_folder_stat_async(file_: Path, storage_stats: dict[Path, FolderInfo]):
    for file_object in file_.iterdir():
        logger.debug(f'File {file_object.name} is processing!')

        abs_path_to_file = await get_abs_name_of_file(file_object)

        if not abs_path_to_file:
            continue

        if await check_dir_is_available(file_object):
            await get_folder_stat_async(file_object, storage_stats)
        else:
            total_files = 1
            total_size = await get_file_size(file_object)
            checksum = await get_file_checksum(file_object)

            if not total_size or not checksum:
                continue

            storage_stats[abs_path_to_file] = FolderInfo(total_files, total_size, checksum)

    generated_stat = await generate_folder_statistics(file_, storage_stats)
    storage_stats[file_.absolute()] = generated_stat

    return generated_stat


async def calculate_stat_async(path: str):
    root_folder = Path(path)
    storage_stats: dict[Path, FolderInfo] = {}

    if not root_folder.exists() or not root_folder.is_dir():
        raise NotADirectoryError('Path does not exists or this is not a directory')

    await asyncio.create_task(get_folder_stat_async(root_folder, storage_stats))
    return storage_stats


PATH_FOR_STAT = '/Users/dzmitryrahozenka'


if __name__ == '__main__':
    res = asyncio.run(calculate_stat_async(PATH_FOR_STAT))
    pprint(res)

