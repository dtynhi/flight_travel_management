import random
import string
from datetime import datetime, timedelta, time


def random_secure_string(length: int) -> str:
    """Generate a random string of length `length`."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def random_secure_code(length: int) -> str:
    """Generate a random code of length `length`."""
    return "".join(random.choices(string.digits, k=length))


def calculate_expire_time(seconds: int) -> datetime:
    """Calculate the expire time based on the current time and the given seconds."""
    return datetime.now() + timedelta(seconds=seconds)


def omit(d: any, keys: list) -> dict:
    # if d not dict convert to dict
    if not isinstance(d, dict):
        d = object_to_dict(d)
    return {k: v for k, v in d.items() if k not in keys}


def pick(d: any, keys: list) -> dict:
    # if d not dict convert to dict
    if not isinstance(d, dict):
        d = object_to_dict(d)
    return {k: v for k, v in d.items() if k in keys}


def copy_property(source: dict, target: dict, includes=None, excludes=None) -> dict:
    includes = includes or []
    excludes = excludes or []

    for k, v in source.items():
        if k in excludes:
            continue
        if includes and k not in includes:
            continue
        if k in target:
            target[k] = v

    return target


def get_timestamp(date_str: str) -> int:
    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
    return int(date_obj.timestamp()) * 1000  # convert to milliseconds


def get_current_timestamp() -> int:
    return int(datetime.now().timestamp()) * 1000  # convert to milliseconds


def get_timestamp_str(date_str: str) -> str:
    return str(get_timestamp(date_str))


def get_current_timestamp_str() -> str:
    return str(get_current_timestamp())


def object_to_dict(obj):
    if not obj:
        return obj
    if isinstance(obj, dict):
        return {key: object_to_dict(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [object_to_dict(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return {key: object_to_dict(value) for key, value in obj.__dict__.items()}
    else:
        return obj


def is_millisecond_timestamp(s):
    if not s.isdigit() or len(s) != 13:
        return False
    try:
        timestamp = int(s)
        min_valid_timestamp = 0
        max_valid_timestamp = int(time.time() * 1000)
        return min_valid_timestamp <= timestamp <= max_valid_timestamp
    except ValueError:
        return False
