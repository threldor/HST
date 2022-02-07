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
import cProfile, pstats


# main
if __name__ == '__main__':

    profiler = cProfile.Profile()
    profiler.enable()

    # load in user specific config
    with open('config.json') as json_file:

        _config = json.load(json_file)

    _path = Path(_config['path'])

    _drive = _config['drive']


    # -- 2-BYTE --

    # setup the input file pointing to the HST_one file (master)

    # inputFile = Path(r'C:\Users\jaun.vanheerden\PycharmProjects\HST\resources\CleanHistory\TestTags2Byte_A'
    #                  r'\TestTag5SecondsInDay.HST')

    inputFile = Path('C:/Users/jaun.vanheerden/PycharmProjects/HST/resources/ST050/ST050PLC01P401asFrequency.HST')

    # create a blank HST_one object to set the drive prior to loading
    hst = HST()

    hst.drive = _drive

    # repath to the following dir, this repath replaces the paths
    # within the HST_one
    # hst.repath = Path(r'C:\Users\jaun.vanheerden\PycharmProjects\HST\resources\converted\2-byte')
    # hst.repath = Path(r'C:\Users\jaun.vanheerden\PycharmProjects\HST\resources\CleanHistory\TestTags2Byte_A')
    hst.repath = Path('C:/Users/jaun.vanheerden/PycharmProjects/HST/resources/ST050')


    # load
    hst.load(inputFile)

    # <single file editing>
    # choose object
    #HST_10 = hst.HSTDataItems[10]

    # modify header
    # as keyword args
    #HST_10.modHeader(sEngUnits='m/s')
    # or as dict
    #HST_10.modHeader({'sEngUnits': 'm/s2'})
    # or as both
    #HST_10.modHeader({'sEngUnits': 'UNIT'}, EngZero=0)

    #HST_10.displayHeader()

    # <time slice editing (multifile)>

    # setup a time span
    start = datetime.datetime(2020, 12, 12, 0, 1, 0)

    end = datetime.datetime(2021, 12, 12, 0, 4, 0)

    # create a slice, very easy non-inclusive end
    # this can also be indexes based from the oldest file start
    # as the offset start - negative indexes allowed
    slice_dt = hst[:]

    #slice_dummy = hst[datetime.datetime(2021, 12, 12, 0, 4, 0)]

    # can now scale this section
    slice_dt.scale(0, 55, 0, 500)

    #V = slice_dt.get_data()


    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()