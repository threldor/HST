""""Jaun van Heerden
X.
Example:
    $ python hst_engine.py
"""


# imports
from HSTMaster import HSTMaster


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

        self.master = master

        self.HSTDataItems = HSTDataItems

        self.start = start

        self.end = end


    def scale(self, o_min: int, o_max: int, n_min: int, n_max: int) -> None:
        """scale"""

        for HSTDataItem in self.HSTDataItems:

            index = 0

            if self.start in HSTDataItem.span:

                index = self.start % HSTDataItem.masterItem['dataLength']

                if self.end in HSTDataItem.span:
                    count = self.end - self.start
                else:
                    count = HSTDataItem.masterItem['dataLength'] - index

            elif self.end in HSTDataItem.span:

                count = self.end % HSTDataItem.masterItem['dataLength']

            else:

                count = HSTDataItem.masterItem['dataLength']

            HSTDataItem.scale_data(index,
                                   count,
                                   o_min,
                                   o_max,
                                   n_min,
                                   n_max)
