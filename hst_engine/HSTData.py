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
# import datetime
from utils.scaling import scale
from functools import reduce
import typing


__author__ = __maintainer__ = ["Jaun van Heerden"]
__version__ = "1.0.0"
__email__ = ["jaun.vanheerden@allianceautomation.com.au"]
__status__ = "Production"


# noinspection PyTypeChecker
class HSTData(object):

    def __init__(self,
                 master: HSTMaster,
                 masterItem: np.void) -> None:

        self.master = master

        self.masterItem = masterItem

        self.dt_header = np.dtype(header_data(master['version']))

        self.filename = Path(bytes_to_str(self.masterItem['name']))

        # self.sampleRate = datetime.timedelta(milliseconds=int(self.masterItem['samplePeriod']))

        self.index: typing.Union[int, None] = None

        self.span: typing.Union[range, None] = None

        self.header = None

        self.dt_data = None

        self.data = None

        self.load()


    def __getitem__(self, subscript):

        if isinstance(subscript, slice):
            # do your handling for a slice object:

            # ignore step
            if subscript.stop is None:

                start_index = (self.masterItem['dataLength'] + subscript.start) % self.masterItem['dataLength']

                return self.get_data(start_index, self.masterItem['dataLength'] - 1 - start_index)

            if subscript.start is None:

                stop_index = (self.masterItem['dataLength'] + subscript.stop) % self.masterItem['dataLength']

                return self.get_data(0, stop_index)

            start_index = (self.masterItem['dataLength'] + subscript.start) % self.masterItem['dataLength']

            stop_index = (self.masterItem['dataLength'] + subscript.stop) % self.masterItem['dataLength']

            if start_index > stop_index:

                _start = self.get_data(start_index, self.masterItem['dataLength'] - 1 - start_index)

                _stop = self.get_data(1, stop_index)

                data = np.append(_start, _stop)

            else:

                data = self.get_data(start_index, stop_index - start_index)

            return data

        else:
            _index = (self.masterItem['dataLength'] + subscript) % self.masterItem['dataLength']

            # Do your handling for a plain index

            return self.get_data(_index, 1)

    # def __setitem__(self, subscript, value):
    #
    #     if isinstance(subscript, slice):
    #         pass
    #
    #     else:
    #
    #         _index = (self.masterItem['dataLength'] + subscript) % self.masterItem['dataLength']
    #
    #         self.set_data(_index, [value])
    #
    #         if isinstance(value, list):
    #
    #             print('list input')


    def __repr__(self):

        return self.filename.name


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


    def get_data(self, index: int, count: int):

        data = np.fromfile(self.filename,
                           dtype=self.dt_data,
                           count=count,
                           offset=self.dt_header.itemsize + self.dt_data.itemsize * index)  # skip header

        # get timestamp
        # for i in range(len(data)):
        #
        #     timestamp_raw = self.masterItem['startTime'] + self.sampleRate.total_seconds() * (i + index)
        #
        #     timestamp = datetime.datetime.utcfromtimestamp(timestamp_raw)

        return data

    # def set_data(self, index: int, data: list) -> None:
    #
    #     with open(self.filename, 'r+b') as f:
    #         f.seek(self.header.itemsize + index)
    #         # f.write(val.to_bytes(2, 'little'))
    #         # f.write(struct.pack("d", floatval))
    #         # f.write(''.join(data).encode('ascii'))
    #         # f.write(data[0].to_bytes(2, 'little'))
    #         f.write(bytearray(data))
    #
    #         # f.write(GATED_DATA_8_HEX)

    def set_index(self, index: int) -> None:
        """sets the relative index based on the order within the `HSTDataItems` list """
        self.index = index

        _spanIndex = self.index * self.master.dataLengthSegment

        self.span = range(_spanIndex, _spanIndex + self.master.dataLengthSegment - 1)


    def scale_data(self,
                   index: int,
                   count: int,
                   o_min: int,
                   o_max: int,
                   n_min: int,
                   n_max: int) -> None:

        with open(self.filename, 'r+b') as f:

            f.seek(self.header.itemsize + index * 2)  # todo optional times 2 or times 8 dependant bytes

            sample = f.read(2 * count)

            data = [int.from_bytes(sample[k:k + 2], 'little') for k in range(0, len(sample), 2)]

            scaled = [int(val) for val in scale(data, o_min, o_max, n_min, n_max)]

            result = [val.to_bytes(2, 'little') for val in scaled]

            f.seek(self.header.itemsize + index * 2)

            f.write(reduce(lambda x, y: x + y, result))


if __name__ == '__main__':

    pass
