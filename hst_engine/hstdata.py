""""Jaun van Heerden
X.
Example:
    $ python hst_engine.py
"""

# imports
from formats import header_data, data_format, EightByteV600, EightByteV531
from pathlib import Path
import numpy as np
from hstmaster import HSTMaster
from utils.str_conversion import bytes_to_str
from pprint import pprint
import os
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

        self.dt_header = np.dtype(header_data(masterItem['version']))

        self.filename: Path = Path(bytes_to_str(self.masterItem['name']))

        self.index: typing.Union[int, None] = None

        self.span: typing.Union[range, None] = None

        self.header = None

        self.bytes: int = None

        self.dt_data = None

        self.data = None

        self.load()


    def __getitem__(self, subscript):

        if isinstance(subscript, slice):
            # do your handling for a slice object:

            if subscript.stop is None and subscript.start is None:

                return self.get_data(0, self.masterItem['dataLength'])

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


    def __repr__(self):

        return self.filename.name

    def displayHeader(self):

        print(*map(lambda x: f'{x[0]}\t{x[-1]}',
                   zip(self.header.dtype.names, self.header)), sep='\n')

    def displayMasterItem(self):

        print(*map(lambda x: f'{x[0]}\t{x[-1]}',
                   zip(self.masterItem.dtype.names, self.masterItem)), sep='\n')

    def load(self):

        # read the HST_one and push to dict

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

            self.bytes = 8 if self.header['version'] in [EightByteV531, EightByteV600] else 2


    def get_data(self, index: int, count: int):
        """

        :param count:
        :type index: object
        """
        data = np.fromfile(self.filename,
                           dtype=self.dt_data,
                           count=count,
                           offset=self.dt_header.itemsize + self.dt_data.itemsize * index)  # skip header

        return data


    def set_index(self, index: int) -> None:
        """sets the relative index based on the order within the `HSTDataItems` list
        :type index: object
        """
        self.index = index

        _spanIndex = self.index * self.master.dataLengthSegment

        self.span = range(_spanIndex, _spanIndex + self.master.dataLengthSegment - 1)


    def modHeader(self, pathMod: Path = None, *args, **kwargs: dict) -> None:
        """
        :param pathMod:
        :param args: object
        :param kwargs: dict

        """

        if pathMod is not None:

            pathMod = pathMod / self.filename.name

        for arg in args:

            kwargs.update(arg)

        for key, value in kwargs.items():

            if key in self.header.dtype.names:

                self.header[key] = value

                with open(pathMod or self.filename, 'r+b') as f:

                    f.seek(0)

                    f.write(self.header.tobytes())

            else:

                print(f'{key} not in header')

    def scale_data(self,
                   index: int,
                   count: int,
                   o_min: int,
                   o_max: int,
                   n_min: int,
                   n_max: int,
                   pathMod: Path = None) -> None:
        """

        :param pathMod:
        :param n_max:
        :param n_min:
        :param o_max:
        :param o_min:
        :param count:
        :param index: object
        """
        if self.bytes == 8:   # temp return on floats

            return

        if pathMod is not None:

            pathMod = pathMod / self.filename.name

        with open(pathMod or self.filename, 'r+b') as f:

            f.seek(self.header.itemsize + index * self.bytes)  # todo optional times 2 or times 8 dependant bytes

            sample = f.read(self.bytes * count)

            if self.bytes == 2:

                data = [int.from_bytes(sample[k:k + self.bytes], 'little') for k in range(0, len(sample), self.bytes)]

            else:

                data = np.frombuffer(sample, dtype='float')

            scaled = [int(val) for val in scale(data, o_min, o_max, n_min, n_max)]

            result = []

            if self.bytes == 2:

                for val in scaled:

                    val = 65535 if val > 65535 else val

                    check = val.to_bytes(self.bytes, 'little')

                    result.append(check)

            else:

                result = np.array(scaled).tobytes()

            f.seek(self.header.itemsize + index * self.bytes)

            if type(result) is not bytes:

                f.write(reduce(lambda x, y: x + y, result))

            else:

                f.write(result)


if __name__ == '__main__':

    pass
