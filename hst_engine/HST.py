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
from HSTMaster import HSTMaster
from HSTData import HSTData
from pathlib import Path
import datetime
from numba.typed import List
from utils.scaling import scale
from HSTSlice import HSTSlice


class HST(object):

    def __init__(self, filename: Path = None) -> None:

        self.HSTMaster = None

        self.HSTDataitems = []

        self.filename = None

        self.drive = None

        self.repath = None

        self.span = None

        self.samplePeriod = None

        self.dataLengthSegment = None

        self.dataLength = None

        if filename is not None:
            self.load(filename)

    def __getitem__(self, subscript):

        if isinstance(subscript, slice):
            # do your handling for a slice object:

            start_index = (self.dataLength + subscript.start) % self.dataLength if subscript.start else None
            stop_index = (self.dataLength + subscript.stop) % self.dataLength if subscript.stop else None

            # ignore step
            if subscript.stop is None:

                #start_index = (self.dataLength* len(self.HSTDataitems) + subscript.start) % self.dataLength

                dataItems = self.get_HSTDataItems(start_index, self.dataLength - 1 - start_index)

            elif subscript.start is None:

                #stop_index = (self.dataLength + subscript.stop) % self.dataLength

                dataItems = self.get_HSTDataItems(0, stop_index)

            elif start_index > stop_index:

                _start = self.get_HSTDataItems(start_index, self.dataLength - 1 - start_index)

                _stop = self.get_HSTDataItems(1, stop_index)

                dataItems = _start + _stop

                #return HSTSlice(self.HSTMaster, dataItems, start_index, stop_index)

            else:

                dataItems = self.get_HSTDataItems(start_index, stop_index - start_index)

            return HSTSlice(self.HSTMaster, dataItems, start_index, stop_index)

        #
        #     return data
        #
        else:

            _index = (self.dataLength + subscript) % self.dataLength

            #Do your handling for a plain index
            dataItems = self.get_HSTDataItems(_index)

            return HSTSlice(self.HSTMaster, dataItems, _index, _index)

    def load(self, filename: Path) -> None:

        self.filename = filename

        self.HSTMaster = HSTMaster(self, self.filename)

        self.HSTDataitems = sorted([HSTData(self.HSTMaster, data) for data in self.HSTMaster.data],
                                   key=lambda x: x.masterItem['startTime'])

        self.samplePeriod = datetime.timedelta(milliseconds=int(self.HSTDataitems[0].masterItem['samplePeriod']))

        self.dataLengthSegment = self.HSTDataitems[0].masterItem['dataLength']

        self.dataLength = self.dataLengthSegment * len(self.HSTDataitems)

        self.span = range(self.HSTDataitems[0].masterItem['startTime'],
                          self.HSTDataitems[0].masterItem['endTime'],
                          int(self.samplePeriod.total_seconds()))


    def get_HSTDataItems(self, start: int, count: int = 1):  # todo

        # find files
        start_index = int(start / self.dataLengthSegment)

        stop_index = int((start + count) / self.dataLengthSegment)

        if start_index != stop_index:
            return self.HSTDataitems[start_index:stop_index + 1]
        else:
            return [self.HSTDataitems[start_index]]




if __name__ == '__main__':
    inputFile = Path('../resources/ST051DOS01FIT0780201acHi.HST')

    hst = HST()

    hst.drive = 'C'

    hst.repath = Path(r'C:\Users\jaun.vanheerden\PycharmProjects\HST\resources\converted')

    hst.load(inputFile)

    slice1 = hst[1]

    slice1.scale(0, 500, 0, 100)

    print(hst[:20161])
    print(hst[-2:])
    print(hst[-50: -10000])
    print(hst[20160])
    print(hst[20161])

    print(scale(List(list(range(0, 1000, 2))), 0, 1000, -100, 100))
