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

        self.HSTDataItems = None

        self.filename = None

        self.drive = None

        self.repath = None

        self.spanTime = None

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


        #     return data

        else:

            _index = (self.dataLength + subscript) % self.dataLength

            # Do your handling for a plain index
            dataItems = self.get_HSTDataItems(_index)

            return HSTSlice(self.HSTMaster, dataItems, _index, _index)

    def load(self, filename: Path) -> None:
        """load the HSTMaster item and children HSTData items"""

        self.filename = filename

        self.HSTMaster = HSTMaster(self, self.filename)

        # sort by `startTime`
        # self.HSTDataItems = sorted([HSTData(self.HSTMaster, data) for data in self.HSTMaster.data],
        #                            key=lambda x: x.masterItem['startTime'])
        self.HSTDataItems = [HSTData(self.HSTMaster, data) for data in self.HSTMaster.data]

        #self.samplePeriod = datetime.timedelta(milliseconds=int(self.HSTDataItems[0].masterItem['samplePeriod']))

        # get the data length segement from the first HSTData item - assume all are the same #todo check this
        self.dataLengthSegment = self.HSTDataItems[0].masterItem['dataLength']

        self.dataLength = self.dataLengthSegment * len(self.HSTDataItems)

        for index, HSTDataItem in enumerate(self.HSTDataItems):
            HSTDataItem.set_index(index)


        # self.spanTime = range(self.HSTDataItems[0].masterItem['startTime'],
        #                       self.HSTDataItems[0].masterItem['endTime'],
        #                       int(self.samplePeriod.total_seconds()))


    def get_HSTDataItems(self, start: int, count: int = 1):  # todo

        # find files
        startIndex = int(start / self.dataLengthSegment)

        stopIndex = int((start + count) / self.dataLengthSegment)

        if startIndex != stopIndex:
            return self.HSTDataItems[startIndex:stopIndex + 1]
        else:
            return [self.HSTDataItems[startIndex]]


if __name__ == '__main__':

    inputFile = Path('../resources/ST051DOS01FIT0780201acHi.HST')

    hst = HST()

    hst.drive = 'C'

    hst.repath = Path(r'C:\Users\jaun.vanheerden\PycharmProjects\HST\resources\converted')

    hst.load(inputFile)

    slice1 = hst[10_000:20_000]

    slice1.scale(0, 500, 0, 100)

    print(hst[:20161])
    print(hst[-2:])
    print(hst[-50: -10000])
    print(hst[20160])
    print(hst[20161])

    print(scale(List(list(range(0, 1000, 2))), 0, 1000, -100, 100))
