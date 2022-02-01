import numpy as np
import datetime
import os


def date_from_webkit(webkit_timestamp):
    epoch_start = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(microseconds=int(webkit_timestamp))
    return epoch_start + delta


def date_to_webkit(date_string):
    epoch_start = datetime.datetime(1601, 1, 1)
    date_ = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    diff = date_ - epoch_start
    seconds_in_day = 60 * 60 * 24
    return '{:<017d}'.format(
        diff.days * seconds_in_day + diff.seconds + diff.microseconds)


# Convert HST_one start/end time into dateTime
def HST_Time_to_datetime(startTime):
    # depending on 2 byte (int32) or 8 byte (int64)
    if startTime.itemsize == 8:
        # 8 byte
        return date_from_webkit(DATAHdata['startTime'] / 10)  # count of 100ns since 1601
    else:
        # 2 byte
        return datetime.datetime.utcfromtimestamp(DATAHdata['startTime'])  # seconds since 1970


# Convert HST_one sample period into dateTime
def HST_Sample_to_datetime(samplePeriod):
    return datetime.timedelta(milliseconds=int(samplePeriod))


inputFile = "resources/ST051DOS01FIT0780201acHi.HST_one"


# inputFile = "converted/8-Byte Trends/ST051DOS01FIT0780201acHi.HST_one"
# inputFile = "D:\\CitectSCADA\\Data\\ST051\\TREND\\ST051DOS01FIT0780201acHi.HST_one"

# given version return data header type
def HSTHeader(v):
    Header2v6 = [('name', '|S144'),
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

    Header2 = [('name', '|S144'),
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

    Header8v6 = [('name', '|S272'),
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

    Header8 = [('name', '|S272'),
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

    # version enumeration
    TwoByteOriginal = 0  # Before v5.00  Header2
    TwoBytePreV500 = 1  # Before v5.00  Header2
    TwoByteV500 = 2  # 5.00 - 5.30   Header2
    TwoByteV531 = 3  # 5.31 - 5.50   Header2
    TwoByteV600 = 5  # 6.00 - ?      Header2v6
    EightByteV531 = 4  # 5.31 - 550    Header8
    EightByteV600 = 6  # 6.00 - ?      Header8v6

    switcher = {
        0: Header2,
        1: Header2,
        2: Header2,
        3: Header2,
        4: Header8,
        5: Header2v6,
        6: Header8v6,
    }

    return switcher.get(v, 'None')


def DataHeader(v):
    Header2v6 = [('title', '|S112'),
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

    Header2 = [('name', '|S112'),
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

    Header8v6 = [('name', '|S112'),
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

    Header8 = [('name', '|S112'),
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

    # version enumeration
    TwoByteOriginal = 0  # Before v5.00  Header2
    TwoBytePreV500 = 1  # Before v5.00  Header2
    TwoByteV500 = 2  # 5.00 - 5.30   Header2
    TwoByteV531 = 3  # 5.31 - 5.50   Header2
    TwoByteV600 = 5  # 6.00 - ?      Header2v6
    EightByteV531 = 4  # 5.31 - 550    Header8
    EightByteV600 = 6  # 6.00 - ?      Header8v6

    switcher = {
        0: Header2,
        1: Header2,
        2: Header2,
        3: Header2,
        4: Header8,
        5: Header2v6,
        6: Header8v6,
    }

    return switcher.get(v, 'None')


def DataData(v):
    Data2 = [('value', np.int16)]

    Data8 = [('value', np.longlong)]

    # version enumeration
    TwoByteOriginal = 0  # Before v5.00  Header2
    TwoBytePreV500 = 1  # Before v5.00  Header2
    TwoByteV500 = 2  # 5.00 - 5.30   Header2
    TwoByteV531 = 3  # 5.31 - 5.50   Header2
    TwoByteV600 = 5  # 6.00 - ?      Header2v6
    EightByteV531 = 4  # 5.31 - 550    Header8
    EightByteV600 = 6  # 6.00 - ?      Header8v6

    switcher = {
        0: Data2,
        1: Data2,
        2: Data2,
        3: Data2,
        4: Data8,
        5: Data2,
        6: Data8,
    }

    return switcher.get(v, 'None')


# reading chuncks
def read_in_chunks(file_object, chunk_size=16):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


# f = open(inputFile, 'rb')
# print(f.read(128))
# for piece in read_in_chunks(f):
#	print(piece)
# f.close()

masterHeader = [('title', '|S128'),
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

# READ THE MASTER HEADER

# set data type
HSTMdt = np.dtype(masterHeader)
# read the HST_one and push to dict
f = np.fromfile(inputFile, dtype=HSTMdt, count=1)
HSTMdata = dict(zip(f.dtype.names, f[0]))

# determine the version and type to create the data array type
version = HSTMdata['version']
nFiles = HSTMdata['nFiles']

print('---MASTER HEADER--- ' + str(HSTMdt.itemsize))

for key, value in HSTMdata.items():
    print(key, ' : ', value)

# now prep to read the HST_one headers for data
HSTHdt = np.dtype(HSTHeader(version))
# read the HST_one data array and push to dict, offset by master header
f = np.fromfile(inputFile, dtype=HSTHdt, count=nFiles, offset=HSTMdt.itemsize)

print('')
print('---DATAAA HEADER--- ' + str(HSTHdt.itemsize))
i = 0
for i in range(len(f)):
    if i >= 1:
        break
    print('')
    print('---DATA FILE HEADER ' + str(i) + '---')
    HSHHdata = dict(zip(f.dtype.names, f[i]))
    for key, value in HSHHdata.items():
        print(key, ' : ', value)
    i += 1

# Now move onto the data files


print('')
print('file path')
print(f[0]['name'].decode('ASCII').strip().strip('\x00'))

# grab the data file
dataFile = f[0]['name']

print(dataFile)
ospath = f[0]['name'].decode('ASCII').strip().strip('\x00').replace('\\', '/')
print(ospath)

ospath = ospath.replace('D:/CitectSCADA/Data/ST051/TREND/', 'resources/converted/')

# opath=os.path.join(*ospath)
# print(opath)
# read the data file header
# set data type
DATAHdt = np.dtype(DataHeader(version))
# read the Data File header and push to dict
f = np.fromfile(ospath, dtype=DATAHdt, count=1)
DATAHdata = dict(zip(f.dtype.names, f[0]))

print('---DATA 0 HEADER--- ' + str(DATAHdt.itemsize))
for key, value in DATAHdata.items():
    print(key, ' : ', value)


def format_sample(value, dataHeader, sampleNo):
    # version enumeration
    TwoByteOriginal = 0  # Before v5.00  Header2
    TwoBytePreV500 = 1  # Before v5.00  Header2
    TwoByteV500 = 2  # 5.00 - 5.30   Header2
    TwoByteV531 = 3  # 5.31 - 5.50   Header2
    TwoByteV600 = 5  # 6.00 - ?      Header2v6
    EightByteV531 = 4  # 5.31 - 550    Header8
    EightByteV600 = 6  # 6.00 - ?      Header8v6

    # non-valid enumeration
    InvalidData8 = -75058848482373  # If 8-byte Trend sample is <NA>, it is recorded as this LONG value instead of a valid DOUBLE
    GatedData8 = -93823560602966  # If 8-byte Trend sample is <GATED>, it is recorded as this LONG value instead of a valid DOUBLE
    InvalidData8Hex = 0xbbbbffffbbbbffff
    GatedData8Hex = 0xaaaaffffaaaaffff
    InvalidData2 = -32001  # Indicates invalid sample <NA> in 2-byte Trend data 0x82ff
    GatedData2 = -32002  # Indicates gated data <GATED> in 2-byte Trend data 0x82fe

    # account for uninitialised data
    format_uninit = " <Uninitialized data>" if sampleNo > dataHeader['filePointer'] else ""

    formatted = ""

    # scale is dictated by value type or version. we use value type
    if dataHeader['version'] == EightByteV531 or dataHeader['version'] == EightByteV600:

        # 8 byte
        if value == InvalidData8:
            formatted = "<NA>"
        else:
            if value == GatedData8:
                formatted = "<GATED>"
            else:
                value = np.frombuffer(value.tobytes(), dtype='float')
                formatted = str(value) + " [" + str(dataHeader['sEngUnits'].decode('ASCII')) + "]"
    else:
        if value == InvalidData2:
            formatted = str(value) + " [<NA>]"
        else:
            if value == GatedData2:
                formatted = str(value) + " [<GATED>]"
            else:
                m = (dataHeader['EngFull'] - dataHeader['EngZero']) / 32000.0
                v = (m * value) + dataHeader['EngZero']
                formatted = str(value) + " [" + str(v) + " " + str(dataHeader['sEngUnits'].decode('ASCII')) + "]"

    return formatted + format_uninit


# now prep to read the data
version = DATAHdata['version']
dataLength = DATAHdata['dataLength']
startTime = HST_Time_to_datetime(DATAHdata['startTime'])
sampleDelta = HST_Sample_to_datetime(DATAHdata['samplePeriod'])

# start Time for file
# different for 2 byte/8 byte

# startTimeTime=date_from_webkit(DATAHdata['startTime']/10)


DATAdt = np.dtype(DataData(version))
# read the HST_one data array and push to dict, offset by data header
f = np.fromfile(ospath, dtype=DATAdt, count=dataLength, offset=DATAHdt.itemsize)

print('---DATAAA DATAAA---')
i = 0
for i in range(len(f)):
    if i >= 14485:
        break
    Datadata = dict(zip(f.dtype.names, f[i]))

    # sample datetime
    sampleTimestamp = startTime + (i * sampleDelta)

    for key, value in Datadata.items():
        if i >= 14465:
            print(i + 1, ' : ', sampleTimestamp, ' : ', format_sample(value, DATAHdata, i + 1))
    i += 1
