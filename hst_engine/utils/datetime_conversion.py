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


def date_from_webkit(webkit_timestamp: str) -> datetime:
    epoch_start = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(microseconds=int(webkit_timestamp))
    return epoch_start + delta


def date_to_webkit(date_string: str) -> str:
    epoch_start = datetime.datetime(1601, 1, 1)
    date_ = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    diff = date_ - epoch_start
    seconds_in_day = 60 * 60 * 24
    return '{:<017d}'.format(
        diff.days * seconds_in_day + diff.seconds + diff.microseconds)


# Convert HST start/end time into dateTime
def HST_Time_to_datetime(DATAHdata: dict, start_time: str) -> datetime:
    # depending on 2 byte (int32) or 8 byte (int64)
    if start_time.itemsize == 8:
        # 8 byte
        return date_from_webkit(DATAHdata['startTime'] / 10)  # count of 100ns since 1601
    else:
        # 2 byte
        return datetime.datetime.utcfromtimestamp(DATAHdata['startTime'])  # seconds since 1970


# Convert HST sample period into dateTime
def HST_Sample_to_datetime(sample_period: str) -> datetime:
    return datetime.timedelta(milliseconds=int(sample_period))



# main

def main():
    pass


if __name__ == "__main__":
    main()
