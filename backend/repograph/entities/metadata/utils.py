"""
Utils for the Metadata entity
"""
import datetime

FORMAT = "%Y-%m-%d %H:%M:%S"


def datetime_to_string(dt: datetime.datetime) -> str:
    """Convert datetime.datetime object to string.

    Args:
        dt (datetime.datetime): Object to convert to string.

    Returns:
        str
    """
    return dt.isoformat(sep=' ', timespec='milliseconds')


def string_to_datetime(string: str) -> datetime.datetime:
    """Convert string to datetime.datetime object.

    Args:
        string (str): String to parse.

    Returns:
        datetime.datetime
    """
    return datetime.datetime.fromisoformat(string)
