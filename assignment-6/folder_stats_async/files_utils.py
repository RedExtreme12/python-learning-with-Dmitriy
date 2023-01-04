from pathlib import Path
import hashlib
import os
import logging

logger = logging.getLogger(f'logger_conf.{__name__}')


async def get_file_size(file_: Path) -> int | None:
    try:
        return file_.stat().st_size
    except OSError as err:
        logger.debug(f'Unable to calculate size of file {file_.name}, because {err.strerror}')
        return None


def get_abs_name_of_file(file_: Path) -> Path | None:
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

    checksum.update(file_.name.encode())
    return checksum.hexdigest()


def update_checksum(file_: Path, checksum_to_update, checksum_from_update: str):
    if checksum_from_update:
        checksum_to_update.update(checksum_from_update.encode())

        # In case the objects is a folder, we must also take into account its name, as in the case of files
        if file_.is_dir():
            checksum_to_update.update(file_.name.encode())

