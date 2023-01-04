from dataclasses import dataclass


@dataclass
class FolderInfo:
    total_files: int
    total_size: int  # in bytes
    check_sum: str
