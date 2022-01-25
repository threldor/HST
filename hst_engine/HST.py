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


class HST(object):

    def __init__(self, filename: Path = None) -> None:

        self.HSTMaster = None

        self.HSTDataitems = []

        self.filename = None

        self.drive = None

        self.repath = None

        self.span = None

        self.samplePeriod = None

        self.dataLength = None

        if filename is not None:
            self.load(filename)

    def __getitem__(self, subscript):

        if isinstance(subscript, slice):
            # do your handling for a slice object:
            pass

        #     # ignore step
        #     if subscript.stop is None:
        #
        #         start_index = (self.masterItem['dataLength'] + subscript.start) % self.masterItem['dataLength']
        #
        #         return self.get_data(start_index, self.masterItem['dataLength'] - 1 - start_index)
        #
        #     if subscript.start is None:
        #
        #         stop_index = (self.masterItem['dataLength'] + subscript.stop) % self.masterItem['dataLength']
        #
        #         return self.get_data(0, stop_index)
        #
        #     start_index = (self.masterItem['dataLength'] + subscript.start) % self.masterItem['dataLength']
        #
        #     stop_index = (self.masterItem['dataLength'] + subscript.stop) % self.masterItem['dataLength']
        #
        #     if start_index > stop_index:
        #
        #         _start = self.get_data(start_index, self.masterItem['dataLength'] - 1 - start_index)
        #
        #         _stop = self.get_data(1, stop_index)
        #
        #         data = np.append(_start, _stop)
        #
        #     else:
        #
        #         data = self.get_data(start_index, stop_index - start_index)
        #
        #     return data
        #
        # else:

        _index = (self.dataLength + subscript) % (self.dataLength * len(self.HSTDataitems))

        # Do your handling for a plain index

        return self.get_data(_index, 1)

    def load(self, filename: Path) -> None:

        self.filename = filename

        self.HSTMaster = HSTMaster(self, self.filename)

        self.HSTDataitems = sorted([HSTData(self.HSTMaster, data) for data in self.HSTMaster.data],
                                   key=lambda x: x.masterItem['startTime'])

        self.samplePeriod = datetime.timedelta(milliseconds=int(self.HSTDataitems[0].masterItem['samplePeriod']))

        self.dataLength = self.HSTDataitems[0].masterItem['dataLength']

        self.span = range(self.HSTDataitems[0].masterItem['startTime'],
                          self.HSTDataitems[0].masterItem['endTime'],
                          int(self.samplePeriod.total_seconds()))


    def get_data(self, start: int, count: int):   # todo

        # find files
        start_index = int(start / self.dataLength)

        stop_index = int((start + count) / self.dataLength)

        if start_index != stop_index:
            dataFiles = self.HSTDataitems[start_index:stop_index]
        else:
            dataFiles = [self.HSTDataitems[start_index]]

        if len(dataFiles) == 1:
            print('single file')
            first = dataFiles[0]
            mid = []
            last = []
        elif len(dataFiles) == 2:
            first, last = dataFiles
            mid = []
        else:
            first, *mid, last = dataFiles
        
        print(first,
              mid,
              last)


if __name__ == '__main__':

    inputFile = Path('../resources/ST051DOS01FIT0780201acHi.HST')

    hst = HST()

    hst.drive = 'C'

    hst.repath = Path(r'C:\Users\jaun.vanheerden\PycharmProjects\HST\resources\converted')

    hst.load(inputFile)

    print(hst[1])
    print(hst[20160])
    print(hst[20161])

    hst.get_data(20160, 20160 * 3 + 5)
