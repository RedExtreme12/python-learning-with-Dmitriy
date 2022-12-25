from pathlib import Path
import hashlib


def get_file_hash(file_: Path) -> str:
    hash_ = hashlib.md5(file_.read_bytes() + file_.name.encode()).hexdigest()

    return hash_
