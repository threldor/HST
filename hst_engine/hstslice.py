""""Jaun van Heerden
X.
Example:
    $ python hst_engine.py
"""


# imports
import datetime
import time

from hstmaster import HSTMaster
from hstdata import HSTData
import shutil
import os

__author__ = __maintainer__ = ["Jaun van Heerden"]
__version__ = "1.0.0"
__email__ = ["jaun.vanheerden@allianceautomation.com.au"]
__status__ = "Production"


class HSTSlice(object):
    """A slice..."""

    def __init__(self,
                 master: HSTMaster,
                 HSTDataItems: list,
                 start: int,
                 end: int,
                 inplace: bool = False,
                 resultFolder: str = "result") -> None:
        """

        :param inplace: bool
        :param master: HSTMaster
        """
        self.master = master

        self.HSTDataItems = HSTDataItems

        self.inplace = inplace

        self.resultFolder = resultFolder

        self.resultPath = None

        if not self.inplace:

            # add folder if does not exist

            self.resultPath = self.master.filename.parent / self.resultFolder

            if not os.path.exists(self.resultPath):

                os.mkdir(self.resultPath)

            # copy HST
            newPath = self.resultPath / self.master.filename.name

            if os.path.exists(newPath):
                os.remove(newPath)

            shutil.copyfile(self.master.filename, newPath)

            # copy .### data to and set dir
            for HSTDataItem in self.HSTDataItems:

                newPath = self.resultPath / HSTDataItem.filename.name

                if os.path.exists(newPath):

                    os.remove(newPath)

                shutil.copyfile(HSTDataItem.filename, newPath)

        self.start = start if start else 0

        self.end = end if end else self.master.dataLength



    def scale(self, o_min: int, o_max: int, n_min: int, n_max: int) -> None:

        """
        :param n_max: int
        :param n_min: int
        :param o_max: int
        :param o_min: int
        """

        for HSTDataItem in self.HSTDataItems:

            index, count = self.index_count(HSTDataItem)

            HSTDataItem.scale_data(index,
                                   count,
                                   o_min,
                                   o_max,
                                   n_min,
                                   n_max,
                                   self.resultPath)

    def offsetToToday(self) -> None:
        """
        Offset the startTime and endTime shifting

        :param offset:
        :return:
        """
        # date today
        todayDate = datetime.date.today()

        # last sample date
        endDate = self.master.latest.date()

        # time offset
        offset = time.mktime(todayDate.timetuple()) - time.mktime(endDate.timetuple())

        for HSTDataItem in self.HSTDataItems:
            HSTDataItem.offsetTime(offset, self.resultPath)

    def offsetTime(self, offset: int) -> None:
        """
        Offset the startTime and endTime

        :param offset:
        :return:
        """

        for HSTDataItem in self.HSTDataItems:
            HSTDataItem.offsetTime(offset, self.resultPath)


    def modHeader(self, *args, **kwargs):
        """

        :type kwargs: object
        :type args: object
        """

        kwargs['pathMod'] = self.resultPath

        for HSTDataItem in self.HSTDataItems:
            
            HSTDataItem.modHeader(args, kwargs)


    def index_count(self, HSTDI: HSTData) -> (int, int):
        """
        :param HSTDI: HSTData
        """

        i = 0

        if self.start in HSTDI.span:

            i = self.start % HSTDI.masterItem['dataLength']

            if self.end in HSTDI.span:

                c = self.end - self.start

            else:

                c = HSTDI.masterItem['dataLength'] - i

        elif self.end in HSTDI.span:

            c = self.end % HSTDI.masterItem['dataLength']

        else:

            c = HSTDI.masterItem['dataLength']

        return i, c


    def get_data(self):
        """

        """
        if len(self.HSTDataItems) == 1:
            data = self.HSTDataItems[0][self.start:self.end]
        elif len(self.HSTDataItems) == 2:
            data = self.HSTDataItems[0][self.start:] + self.HSTDataItems[0][:self.end]
        else:
            data = [item[0] for item in self.HSTDataItems[0][self.start:]] + \
                   [item[0] for HSTDataItem in self.HSTDataItems[1:-1] for item in HSTDataItem[:]] + \
                   [item[0] for item in self.HSTDataItems[0][:self.end]]


        return [data, list(range(self.start, self.end, self.master.samplePeriod))]


    def modMasterHST(self, *args, **kwargs):
        self.master.modHSTHeader(args, kwargs)

    def modMasterHSTDataItem(self, index, *args, **kwargs):
        self.master.modHSTDataItem(index, args, kwargs)

    def modMasterHSTDataItems(self, *args, **kwargs):
        self.master.modHSTDataItems(args, kwargs)