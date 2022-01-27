""""Jaun van Heerden
X.
Example:
    $ python hst_engine.py
"""

# imports
from formats import header_data, data_format
from pathlib import Path
import numpy as np
from HSTMaster import HSTMaster
from utils.str_conversion import bytes_to_str
from pprint import pprint
import os
import datetime
from utils.scaling import scale
from functools import reduce

from static import GATED_DATA_8_HEX
from utils.datetime_conversion import HST_Time_to_datetime, HST_Sample_to_datetime
from typing import Union
from numpy.core.multiarray import ndarray
from numpy.typing import _64Bit

__author__ = __maintainer__ = ["Jaun van Heerden"]
__version__ = "1.0.0"
__email__ = ["jaun.vanheerden@allianceautomation.com.au"]
__status__ = "Production"


class HSTSlice(object):

    def __init__(self,
                 master: HSTMaster,
                 HSTDataItems: list,
                 start: int,
                 end: int) -> None:

        self.master = master

        self.HSTDataItems = HSTDataItems

        self.start = start

        self.end = end


    def scale(self, o_min, o_max, n_min, n_max):

        for HSTDataItem in self.HSTDataItems:

            if self.start in HSTDataItem.span:
                residual = self.start % HSTDataItem.masterItem['dataLength']
                HSTDataItem.scale_data(residual,
                                       HSTDataItem.masterItem['dataLength'] - residual,
                                       o_min,
                                       o_max,
                                       n_min,
                                       n_max)

            elif self.end in HSTDataItem.span:
                residual = self.end % HSTDataItem.masterItem['dataLength']
                HSTDataItem.scale_data(0,
                                       residual,
                                       o_min,
                                       o_max,
                                       n_min,
                                       n_max)
            else:
                HSTDataItem.scale_data(0,
                                       HSTDataItem.masterItem['dataLength'],
                                       o_min,
                                       o_max,
                                       n_min,
                                       n_max)




