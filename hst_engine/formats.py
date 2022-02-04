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
import numpy as np

# versions
TwoByteOriginal = 0  # Before v5.00  Header2
TwoBytePreV500 = 1  # Before v5.00  Header2
TwoByteV500 = 2  # 5.00 - 5.30   Header2
TwoByteV531 = 3  # 5.31 - 5.50   Header2
TwoByteV600 = 5  # 6.00 - ?      Header2v6
EightByteV531 = 4  # 5.31 - 550    Header8
EightByteV600 = 6  # 6.00 - ?      Header8v6

# non-valid enumeration
# If 8-byte Trend sample is <NA>
# it is recorded as this LONG value instead of a valid DOUBLE
InvalidData8 = -75058848482373
# If 8-byte Trend sample is <GATED>
# it is recorded as this LONG value instead of a valid DOUBLE
GatedData8 = -93823560602966
InvalidData8Hex = 0xbbbbffffbbbbffff
GatedData8Hex = 0xaaaaffffaaaaffff
InvalidData2 = -32001  # Indicates invalid sample <NA> in 2-byte Trend data 0x82ff
GatedData2 = -32002  # Indicates gated data <GATED> in 2-byte Trend data 0x82fe


# header formats

# MASTER

MASTER_H = [('title', '|S128'),
            ('ID', '|S8'),
            ('filetype', np.int16),
            ('version', np.int16),
            ('alignment1', '|S4'),
            ('mode', np.int32),
            ('history', np.int16),
            ('nFiles', np.int16),
            ('next', np.int16),
            ('addOn', np.int16),
            ('alignment2', '|S20')]

HEADER_2v6 = [('name', '|S144'),
              ('ID', '|S8'),
              ('filetype', np.int16),
              ('version', np.int16),
              ('startEvNo', np.int32),
              ('logName', '|S80'),
              ('mode', np.int32),
              ('area', np.int16),
              ('priv', np.int16),
              ('hystoryType', np.int16),
              ('samplePeriod', np.int32),
              ('sEngUnits', '|S8'),
              ('format', np.int32),
              ('startTime', np.int32),
              ('endTime', np.int32),
              ('dataLength', np.int32),
              ('filePointer', np.int32),
              ('endEvNo', np.int32),
              ('alignment1', '|S2')]

HEADER_2 = [('name', '|S144'),
            ('ID', '|S8'),
            ('filetype', np.int16),
            ('version', np.int16),
            ('startEvNo', np.int32),
            ('logName', '|S32'),
            ('mode', np.int32),
            ('area', np.int16),
            ('priv', np.int16),
            ('hystoryType', np.int16),
            ('samplePeriod', np.int32),
            ('sEngUnits', '|S8'),
            ('format', np.int32),
            ('startTime', np.int32),
            ('endTime', np.int32),
            ('dataLength', np.int32),
            ('filePointer', np.int32),
            ('endEvNo', np.int32),
            ('alignment1', '|S2')]

HEADER_8v6 = [('name', '|S272'),
              ('ID', '|S8'),
              ('filetype', np.int16),
              ('version', np.int16),
              ('startEvNo', np.int64),
              ('alignment1', '|S12'),
              ('logName', '|S80'),
              ('mode', np.int32),
              ('area', np.int16),
              ('priv', np.int16),
              ('hystoryType', np.int16),
              ('samplePeriod', np.int32),
              ('sEngUnits', '|S8'),
              ('format', np.int32),
              ('startTime', np.int64),
              ('endTime', np.int64),
              ('dataLength', np.int32),
              ('filePointer', np.int32),
              ('endEvNo', np.int64),
              ('alignment2', '|S6')]

HEADER_8 = [('name', '|S272'),
            ('ID', '|S8'),
            ('filetype', np.int16),
            ('version', np.int16),
            ('startEvNo', np.int64),
            ('alignment1', '|S12'),
            ('logName', '|S64'),
            ('mode', np.int32),
            ('area', np.int16),
            ('priv', np.int16),
            ('hystoryType', np.int16),
            ('samplePeriod', np.int32),
            ('sEngUnits', '|S8'),
            ('format', np.int32),
            ('startTime', np.int64),
            ('endTime', np.int64),
            ('dataLength', np.int32),
            ('filePointer', np.int32),
            ('endEvNo', np.int64),
            ('alignment2', '|S6')]

# data formats

DATA_H_2v6 = [('name', '|S112'),
              ('RawZero', np.single),
              ('RawFull', np.single),
              ('EngZero', np.single),
              ('EngFull', np.single),
              ('ID', '|S8'),
              ('filetype', np.int16),
              ('version', np.int16),
              ('startEvNo', np.int32),
              ('logName', '|S80'),
              ('mode', np.int32),
              ('area', np.int16),
              ('priv', np.int16),
              ('hystoryType', np.int16),
              ('samplePeriod', np.int32),
              ('sEngUnits', '|S8'),
              ('format', np.int32),
              ('startTime', np.int32),
              ('endTime', np.int32),
              ('dataLength', np.int32),
              ('filePointer', np.int32),
              ('endEvNo', np.int32),
              ('alignment1', '|S2')]

DATA_H_2 = [('name', '|S112'),
            ('RawZero', np.single),
            ('RawFull', np.single),
            ('EngZero', np.single),
            ('EngFull', np.single),
            ('ID', '|S8'),
            ('filetype', np.int16),
            ('version', np.int16),
            ('startEvNo', np.int32),
            ('logName', '|S32'),
            ('mode', np.int32),
            ('area', np.int16),
            ('priv', np.int16),
            ('hystoryType', np.int16),
            ('samplePeriod', np.int32),
            ('sEngUnits', '|S8'),
            ('format', np.int32),
            ('startTime', np.int32),
            ('endTime', np.int32),
            ('dataLength', np.int32),
            ('filePointer', np.int32),
            ('endEvNo', np.int32),
            ('alignment1', '|S2')]

DATA_H_8v6 = [('name', '|S112'),
              ('RawZero', np.single),
              ('RawFull', np.single),
              ('EngZero', np.single),
              ('EngFull', np.single),
              ('ID', '|S8'),
              ('filetype', np.int16),
              ('version', np.int16),
              ('startEvNo', np.int64),
              ('alignment1', '|S12'),
              ('logName', '|S80'),
              ('mode', np.int32),
              ('area', np.int16),
              ('priv', np.int16),
              ('hystoryType', np.int16),
              ('samplePeriod', np.int32),
              ('sEngUnits', '|S8'),
              ('format', np.int32),
              ('startTime', np.int64),
              ('endTime', np.int64),
              ('dataLength', np.int32),
              ('filePointer', np.int32),
              ('endEvNo', np.int64),
              ('alignment2', '|S6')]

DATA_H_8 = [('name', '|S112'),
            ('RawZero', np.single),
            ('RawFull', np.single),
            ('EngZero', np.single),
            ('EngFull', np.single),
            ('ID', '|S8'),
            ('filetype', np.int16),
            ('version', np.int16),
            ('startEvNo', np.int64),
            ('alignment1', '|S12'),
            ('logName', '|S64'),
            ('mode', np.int32),
            ('area', np.int16),
            ('priv', np.int16),
            ('hystoryType', np.int16),
            ('samplePeriod', np.int32),
            ('sEngUnits', '|S8'),
            ('format', np.int32),
            ('startTime', np.int64),
            ('endTime', np.int64),
            ('dataLength', np.int32),
            ('filePointer', np.int32),
            ('endEvNo', np.int64),
            ('alignment2', '|S6')]


# given version return data header type
def header_HST(v: int) -> list:
    """x"""

    # version enumeration
    # TwoByteOriginal = 0  # Before v5.00  Header2
    # TwoBytePreV500 = 1  # Before v5.00  Header2
    # TwoByteV500 = 2  # 5.00 - 5.30   Header2
    # TwoByteV531 = 3  # 5.31 - 5.50   Header2
    # TwoByteV600 = 5  # 6.00 - ?      Header2v6
    # EightByteV531 = 4  # 5.31 - 550    Header8
    # EightByteV600 = 6  # 6.00 - ?      Header8v6

    switcher = {
        0: HEADER_2,
        1: HEADER_2,
        2: HEADER_2,
        3: HEADER_2,
        4: HEADER_8,
        5: HEADER_2v6,
        6: HEADER_8v6,
    }

    return switcher.get(v, None)


def header_data(v: int) -> list:
    """x"""

    # version enumeration
    # TwoByteOriginal = 0  # Before v5.00  Header2
    # TwoBytePreV500 = 1  # Before v5.00  Header2
    # TwoByteV500 = 2  # 5.00 - 5.30   Header2
    # TwoByteV531 = 3  # 5.31 - 5.50   Header2
    # TwoByteV600 = 5  # 6.00 - ?      Header2v6
    # EightByteV531 = 4  # 5.31 - 550    Header8
    # EightByteV600 = 6  # 6.00 - ?      Header8v6

    switcher = {
        0: DATA_H_2,
        1: DATA_H_2,
        2: DATA_H_2,
        3: DATA_H_2,
        4: DATA_H_8,
        5: DATA_H_2v6,
        6: DATA_H_8v6,
    }

    return switcher.get(v, None)


def data_format(v: int) -> list:
    """x"""

    Data2 = [('value', np.int16)]

    Data8 = [('value', np.longlong)]

    # version enumeration
    # TwoByteOriginal = 0  # Before v5.00  Header2
    # TwoBytePreV500 = 1  # Before v5.00  Header2
    # TwoByteV500 = 2  # 5.00 - 5.30   Header2
    # TwoByteV531 = 3  # 5.31 - 5.50   Header2
    # TwoByteV600 = 5  # 6.00 - ?      Header2v6
    # EightByteV531 = 4  # 5.31 - 550    Header8
    # EightByteV600 = 6  # 6.00 - ?      Header8v6

    switcher = {
        0: Data2,
        1: Data2,
        2: Data2,
        3: Data2,
        4: Data8,
        5: Data2,
        6: Data8,
    }

    return switcher.get(v, None)
