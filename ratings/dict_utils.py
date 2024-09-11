"""
This module contains functions that extract values from dictionaries.
It's intended to be used in the ratings package.
"""

from datetime import datetime
from typing import Optional

def read_str_value(record: dict, key: str, default_value: str = '') -> str:
    """
    Reads a string value from a record.
    """
    if not key in record:
        return default_value

    value = record.get(key)
    if value is None:
        return default_value

    if isinstance(value, str):
        value = value.strip()

    return value


def read_int_value(record: dict, key: str, default_value: int = 0) -> int:
    """
    Reads an integer value from a record.
    """
    str_value = read_str_value(record, key)

    if str_value == '':
        return default_value

    value = int(str_value)

    return value

def read_datetime_value(record: dict, key: str, default_value = None) -> Optional[datetime]:
    """
    Reads a datetime value from a record.
    """
    date_format = '%Y-%m-%dT%H:%M:%S'
    str_value = read_str_value(record, key)

    if str_value == '':
        return default_value

    value = datetime.strptime(str_value, date_format)

    return value
