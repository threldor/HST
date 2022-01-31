""""Jaun van Heerden
X.
Example:
    $ python hst_engine.py
"""

__author__ = __maintainer__ = ["Jaun van Heerden"]
__version__ = "1.0.0"
__email__ = ["jaun.vanheerden@allianceautomation.com.au"]
__status__ = "Production"

# imports
import datetime
import numpy as np


def date_from_webkit(webkit_timestamp: str) -> datetime:
    """x :type webkit_timestamp: str

    Args:
        webkit_timestamp (str):
    """
    epoch_start = datetime.datetime(1601, 1, 1)

    delta = datetime.timedelta(microseconds=int(webkit_timestamp))

    return epoch_start + delta


def date_to_webkit(date_string: str) -> str:
    """x

    Args:
        date_string (str):
    """
    epoch_start = datetime.datetime(1601, 1, 1)

    date_ = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

    diff = date_ - epoch_start

    seconds_in_day = 60 * 60 * 24

    return '{:<017d}'.format(
        diff.days * seconds_in_day + diff.seconds + diff.microseconds)


# Convert HST start/end time into dateTime
def HST_Time_to_datetime(startTime: np.int32) -> datetime:
    """
    Args:
        startTime (np.int32):
    """

    print(type(startTime))

    # depending on 2 byte (int32) or 8 byte (int64)
    if startTime.itemsize == 8:
        # 8 byte
        return date_from_webkit(startTime / 10)  # count of 100ns since 1601
    else:
        # 2 byte
        return datetime.datetime.utcfromtimestamp(startTime)  # seconds since 1970


# Convert HST sample period into dateTime
def HST_Sample_to_datetime(sample_period: str) -> datetime:
    """x

    Args:
        sample_period (str):
    """
    return datetime.timedelta(milliseconds=int(sample_period))


def datetime_to_index(dt: datetime.datetime, earliest: datetime.datetime, increment: int = 1) -> int:
    """x

    Args:
        dt (datetime.datetime):
        earliest (datetime.datetime):
        increment (int):
    """
    # difference divided by increment
    return int((dt - earliest).total_seconds() / increment)


if __name__ == "__main__":
    pass
