from typing import List
import os


def ensure_directories_present(directories: List[str]):
    for directory in directories:
        ensure_directory_present(dir=directory)


def ensure_directory_present(dir: str):
    if not os.path.exists(dir):
        os.mkdir(dir)
