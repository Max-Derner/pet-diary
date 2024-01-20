from datetime import datetime, timezone
import os
from typing import List
from json import JSONEncoder
from decimal import Decimal


def ensure_directories_present(directories: List[str]):
    for directory in directories:
        ensure_directory_present(dir=directory)


def ensure_directory_present(dir: str):
    if not os.path.exists(dir):
        os.mkdir(dir)


def utc_timestamp_now() -> float:
    return utc_datetime_now().timestamp()


def utc_datetime_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def british_format_time(timestamp: float) -> str:
    """Gives format in the style: Friday, 24 November 2023 - 05:35PM"""
    if not isinstance(timestamp, float):
        timestamp = float(timestamp)  # Don't error catch, what's the alternative?
    return datetime.fromtimestamp(timestamp).strftime('%A, %-d %B %Y - %I:%M %p')


def current_date() -> str:
    # Gives format in the style: Friday, 24 November 2023
    current_date = utc_datetime_now().date()
    return current_date.strftime('%A, %-d %B %Y')


class DynamoItemJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)
