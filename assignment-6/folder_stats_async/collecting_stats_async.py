from .files_utils import (
    get_file_size, get_abs_name_of_file,
    check_dir_is_available, get_file_checksum,
    update_checksum
)
from .folder_info import FolderInfo

from pathlib import Path
import asyncio
import logging
import hashlib

logger = logging.getLogger(f'logger_conf.{__name__}')


def generate_folder_statistics(folder: Path, storage_stats: dict[Path, FolderInfo]) -> FolderInfo:
    total_files = 0
    total_size = 0
    checksum_folder = hashlib.md5()

    for file_obj in folder.iterdir():
        file_obj_stat = storage_stats.get(file_obj.absolute())

        if file_obj_stat:
            total_files += file_obj_stat.total_files
            total_size += file_obj_stat.total_size

            update_checksum(file_obj, checksum_folder, file_obj_stat.check_sum)

    checksum_folder.update(folder.name.encode())

    folder_stat = FolderInfo(total_files, total_size, checksum_folder.hexdigest())
    return folder_stat


async def get_folder_stat_async(file_: Path, storage_stats: dict[Path, FolderInfo]):
    for file_object in file_.iterdir():
        logger.debug(f'File {file_object.name} is processing!')

        abs_path_to_file = get_abs_name_of_file(file_object)

        if not abs_path_to_file:
            continue

        if await check_dir_is_available(file_object):
            await get_folder_stat_async(file_object, storage_stats)
        else:
            total_files = 1
            total_size = await get_file_size(file_object)
            checksum = await get_file_checksum(file_object)

            if total_size is None or checksum is None:
                continue

            storage_stats[abs_path_to_file] = FolderInfo(total_files, total_size, checksum)

    generated_stat = generate_folder_statistics(file_, storage_stats)
    storage_stats[get_abs_name_of_file(file_)] = generated_stat

    return generated_stat


async def calculate_stat_async(root_folder: Path):
    storage_stats: dict[Path, FolderInfo] = {}

    if not root_folder.exists() or not root_folder.is_dir():
        raise NotADirectoryError('Path does not exists or this is not a directory')

    await asyncio.create_task(get_folder_stat_async(root_folder, storage_stats))
    return storage_stats


def get_summary_stat(path: str) -> FolderInfo:
    """
    Returns statistics on the folder to which the path was passed
    param path: str, path to folder
    return: FolderInfo object with stat
    """
    root_folder = Path(path)
    stats = asyncio.run(calculate_stat_async(root_folder))

    return stats[root_folder]
