from pathlib import Path
import hashlib


def get_file_hash(file_: Path) -> str | None:
    checksum = hashlib.md5()

    try:
        with file_.open('rb') as file_cursor:
            while True:
                chunk = file_cursor.read(4096)
                if not chunk:
                    break
                checksum.update(chunk)
    except OSError as err:
        return None

    checksum.update(file_.name.encode())
    return checksum.hexdigest()
