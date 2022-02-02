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
from hstmaster import HSTMaster
from hstdata import HSTData
from pathlib import Path
import datetime
from numba.typed import List
# from hst_engine.utils.scaling import scale
from hstslice import HSTSlice
import typing
from utils.datetime_conversion import datetime_to_index


class HST(object):

    def __init__(self, filename: Path = None) -> None:
        """

        :type filename: Path
        """
        self.HSTMaster = None

        self.HSTDataItems = None

        self.filename = None

        self.drive = None

        self.repath = None

        self.samplePeriod = None

        self.dataLengthSegment = None

        self.dataLength = None

        if filename is not None:

            self.load(filename)

    def __getitem__(self, subscript):

        # check to see if first need to convert datetime to index
        subscript = self.subscript_process(subscript)

        if isinstance(subscript, slice):
            # do your handling for a slice object:

            start_index = (self.dataLength + subscript.start) % self.dataLength if subscript.start else None

            stop_index = (self.dataLength + subscript.stop) % self.dataLength if subscript.stop else None

            # ignore step
            if subscript.stop is None:

                dataItems = self.get_HSTDataItems(start_index, self.dataLength - 1 - start_index)

            elif subscript.start is None:

                dataItems = self.get_HSTDataItems(0, stop_index)

            elif start_index > stop_index:

                _start = self.get_HSTDataItems(start_index, self.dataLength - 1 - start_index)

                _stop = self.get_HSTDataItems(1, stop_index)

                dataItems = _start + _stop

            else:

                dataItems = self.get_HSTDataItems(start_index, stop_index - start_index)

            return HSTSlice(self.HSTMaster, dataItems, start_index, stop_index)

        else:

            _index = (self.dataLength + subscript) % self.dataLength

            # Do your handling for a plain index
            dataItems = self.get_HSTDataItems(_index)

            return HSTSlice(self.HSTMaster, dataItems, _index, _index)

    def load(self, filename: Path) -> None:
        """load the HSTMaster item and children HSTData items
        :type filename: object
        """

        self.filename = filename

        self.HSTMaster = HSTMaster(self, self.filename)

        self.HSTDataItems = [HSTData(self.HSTMaster, data) for data in self.HSTMaster.data]

        # get the data length segment from the first HSTData item - assume all are the same #todo check this
        self.dataLengthSegment = self.HSTDataItems[0].masterItem['dataLength']

        self.dataLength = self.dataLengthSegment * len(self.HSTDataItems)

        for index, HSTDataItem in enumerate(self.HSTDataItems):

            HSTDataItem.set_index(index)


    def get_HSTDataItems(self, start_index: int, count: int = 1):
        """

        :param count: 
        :type start_index: object
        """
        # find files
        startIndex = int(start_index / self.dataLengthSegment)

        stopIndex = int((start_index + count) / self.dataLengthSegment)

        if startIndex != stopIndex:

            return self.HSTDataItems[startIndex:stopIndex + 1]

        else:

            return [self.HSTDataItems[startIndex]]


    def subscript_process(self, subscript: typing.Union[datetime.datetime, slice]):
        """x
        :type subscript: object
        """
        if isinstance(subscript, slice):

            _start = subscript.start

            _stop = subscript.stop

            if isinstance(_start, datetime.datetime):

                _start = datetime_to_index(_start, self.HSTMaster.earliest, 30)

            if isinstance(_stop, datetime.datetime):

                _stop = datetime_to_index(_stop, self.HSTMaster.earliest, 30)

            return slice(_start, _stop)

        else:
            
            if isinstance(subscript, datetime.datetime):

                return datetime_to_index(subscript, self.HSTMaster.earliest, 30)

        return subscript



if __name__ == '__main__':

    # setup the input file pointing to the HST_one file (master)
    inputFile = Path('../resources/converted/2-byte/ST051DOS01FIT0780201acHi.HST')

    # create a blank HST_one object to set the drive prior to loading
    hst = HST_one()

    hst.drive = 'C'

    # repath to the following dir, this repath replaces the paths
    # within the HST_one
    hst.repath = Path(r'C:\Users\jaun.vanheerden\PycharmProjects\HST\resources\converted\2-byte')

    # load
    hst.load(inputFile)

    # <single file editing>
    # choose object
    HST_10 = hst.HSTDataItems[10]

    # modify header
    # as keyword args
    #HST_10.modHeader(EngFull=1000)
    #HST_10.modHeader(endTime=131337503700000010)
    # or as dict
    HST_10.modHeader({'sEngUnits': 'm/s2'})
    # or as both
    HST_10.modHeader({'sEngUnits': 'UNIT'}, EngZero=0)

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
