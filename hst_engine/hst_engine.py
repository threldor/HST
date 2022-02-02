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
from pathlib import Path
from hst import HST
import datetime
import json

# main
if __name__ == '__main__':

    # load in user specific config
    with open('config.json') as json_file:

        _config = json.load(json_file)

    _path = Path(_config['path'])


    # -- 2-BYTE --

    # setup the input file pointing to the HST_one file (master)
    # inputFile = Path('../resources/converted/2-byte/ST051DOS01FIT0780201acHi.HST')

    inputPath_2 = _path / 'resources/converted/2-byte'

    inputFile_2 = inputPath_2 / 'ST051DOS01FIT0780201acHi.HST'

    # create a blank HST_one object to set the drive prior to loading
    hst = HST()

    hst.drive = 'C'

    # repath to the following dir, this repath replaces the paths
    # within the HST_one
    hst.repath = inputPath_2

    # load
    hst.load(inputFile_2)

    # <single file editing>
    # choose object
    HST_10 = hst.HSTDataItems[10]

    # modify header
    # as keyword args
    HST_10.modHeader(sEngUnits='m/s')
    # or as dict
    HST_10.modHeader({'sEngUnits': 'm/s2'})
    # or as both
    HST_10.modHeader({'sEngUnits': 'UNIT'}, EngZero=0)

    HST_10.displayHeader()

    # <time slice editing (multifile)>

    # setup a time span
    start = datetime.datetime(2020, 12, 12, 0, 1, 0)

    end = datetime.datetime(2021, 12, 12, 0, 4, 0)

    # create a slice, very easy non-inclusive end
    # this can also be indexes based from the oldest file start
    # as the offset start - negative indexes allowed
    slice_dt = hst[start:end]

    # can now scale this section
    slice_dt.scale(0, 100, 0, 1000)

    V = slice_dt.get_data()


    # -- 8-BYTE --

    # setup the input file pointing to the HST_one file (master)
    inputPath_8 = _path / 'resources/converted/8-byte'

    inputFile_8 = inputPath_8 / 'ST051DOS01FIT0780201acHi.HST'

    # create a blank HST_one object to set the drive prior to loading
    hst = HST()

    hst.drive = 'C'

    # repath to the following dir, this repath replaces the paths
    # within the HST_one
    hst.repath = inputPath_8

    # load
    hst.load(inputFile_8)

    # <single file editing>
    # choose object
    HST_10 = hst.HSTDataItems[10]

    # modify header
    # as keyword args
    HST_10.modHeader(sEngUnits='m/s')
    # or as dict
    HST_10.modHeader({'sEngUnits': 'm/s2'})
    # or as both
    HST_10.modHeader({'sEngUnits': 'UNIT'}, EngZero=0)

    HST_10.displayHeader()

    # <time slice editing (multifile)>

    # setup a time span
    start = datetime.datetime(2020, 12, 12, 0, 1, 0)

    end = datetime.datetime(2021, 12, 12, 0, 4, 0)

    # create a slice, very easy non-inclusive end
    # this can also be indexes based from the oldest file start
    # as the offset start - negative indexes allowed
    slice_dt = hst[start:end]

    # can now scale this section
    slice_dt.scale(0, 100, 0, 1000)
