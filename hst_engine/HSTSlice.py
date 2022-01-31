""""Jaun van Heerden
X.
Example:
    $ python hst_engine.py
"""


# imports
from HSTMaster import HSTMaster
from HSTData import HSTData

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
                 end: int) -> None:
        """

        :type master: HSTMaster
        """
        self.master = master

        self.HSTDataItems = HSTDataItems

        self.start = start

        self.end = end


    def __str__(self):

        for HSTDataItem in self.HSTDataItems:

            index, count = self.index_count(HSTDataItem)

            print(HSTDataItem)

            index = 0

            # if self.start in HSTDataItem.span:
            #
            #     index = self.start % HSTDataItem.masterItem['dataLength']
            #
            #     if self.end in HSTDataItem.span:
            #         count = self.end - self.start
            #     else:
            #         count = HSTDataItem.masterItem['dataLength'] - index
            #
            # elif self.end in HSTDataItem.span:
            #
            #     count = self.end % HSTDataItem.masterItem['dataLength']
            #
            # else:
            #
            #     count = HSTDataItem.masterItem['dataLength']

            print(HSTDataItem[index:index + count])



    def scale(self, o_min: int, o_max: int, n_min: int, n_max: int) -> None:

        """
        :param n_max: int
        :param n_min: int
        :param o_max: int
        :param o_min: int
        """

        for HSTDataItem in self.HSTDataItems:

            index, count = self.index_count(HSTDataItem)

            # index = 0
            #
            # if self.start in HSTDataItem.span:
            #
            #     index = self.start % HSTDataItem.masterItem['dataLength']
            #
            #     if self.end in HSTDataItem.span:
            #         count = self.end - self.start
            #     else:
            #         count = HSTDataItem.masterItem['dataLength'] - index
            #
            # elif self.end in HSTDataItem.span:
            #
            #     count = self.end % HSTDataItem.masterItem['dataLength']
            #
            # else:
            #
            #     count = HSTDataItem.masterItem['dataLength']

            HSTDataItem.scale_data(index,
                                   count,
                                   o_min,
                                   o_max,
                                   n_min,
                                   n_max)


    def index_count(self, HSTDI: HSTData) -> (int, int):
        """
        :type HSTDI: HSTData
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
