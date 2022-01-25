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
from utils.datetime_conversion import HST_Time_to_datetime, HST_Sample_to_datetime
from typing import Union
from numpy.core.multiarray import ndarray
from numpy.typing import _64Bit


__author__ = __maintainer__ = ["Jaun van Heerden"]
__version__ = "1.0.0"
__email__ = ["jaun.vanheerden@allianceautomation.com.au"]
__status__ = "Production"


class HSTData(object):


    def __init__(self,
                 master: HSTMaster,
                 masterItem: np.void) -> None:

        self.master = master

        self.masterItem = masterItem

        self.dt_header = np.dtype(header_data(master['version']))

        self.filename = Path(bytes_to_str(self.masterItem['name']))

        self.header = None

        self.dt_data = None

        self.data = None

        self.load()


    def __getitem__(self, subscript):

        if isinstance(subscript, slice):
            # do your handling for a slice object:

            # ignore step

            start_index = (self.masterItem['dataLength'] + subscript.start) % self.masterItem['dataLength']

            stop_index = (self.masterItem['dataLength'] + subscript.stop) % self.masterItem['dataLength']

            if start_index > stop_index:

                _start = self.get_data(start_index, self.masterItem['dataLength'] - 1 - start_index)

                _stop = self.get_data(1, stop_index)

                data = np.append(_start, _stop)

            else:

                data = self.get_data(start_index, stop_index)

            return data

        else:

            # Do your handling for a plain index

            return np.fromfile(self.filename,
                               dtype=self.dt_data,
                               count=1,
                               offset=self.dt_header.itemsize + self.dt_data.itemsize * subscript)


    def load(self):

        # read the HST and push to dict

        try:

            if self.master.parent.drive is not None:

                self.filename = Path(f"{self.master.parent.drive}:{os.path.splitdrive(self.filename)[-1]}")

            if self.master.parent.repath is not None:

                self.filename = self.master.parent.repath / self.filename.name

            self.header = np.fromfile(self.filename, dtype=self.dt_header, count=1)[0]

        except FileNotFoundError as e:

            print(e)

        if self.header is not None:

            self.dt_data = np.dtype(data_format(self.header['version']))

            pprint(self.header)

            # version = self.header['version']
            # dataLength = self.header['dataLength']
            # startTime = HST_Time_to_datetime(self.header['startTime'])
            # sampleDelta = HST_Sample_to_datetime(self.header['samplePeriod'])


    def get_data(self, index: int, count: int) -> Union[ndarray, ndarray[Union[np.floating[_64Bit], np.float_]]]:

        return np.fromfile(self.filename,
                           dtype=self.dt_data,
                           count=count,
                           offset=self.dt_header.itemsize + self.dt_data.itemsize * index)  # skip header


if __name__ == '__main__':

    hst_header = HSTData()
