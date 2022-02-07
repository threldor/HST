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
from utils.scaling import scale, scale_float
from functools import reduce
import typing
from copy import copy
import struct
from numba import njit

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

    def offsetTime(self, offset: int, pathMod: Path = None) -> None:
        """
        Offset the startTime and endTime

        :param offset:
        :return:
        """
        self.modHeader({'pathMod': pathMod}, startTime=self.header['startTime'] + offset,
                       endTime=self.header['endTime'] + offset)

    def modHeader(self, *args, **kwargs: dict) -> None:
        """
        :param pathMod:
        :param args: object
        :param kwargs: dict

        """

        for arg in args:

            if isinstance(arg, tuple):
                for element in arg:
                    kwargs.update(element)
            else:

                kwargs.update(arg)

        pathMod = None

        if 'pathMod' in kwargs:
            pathMod = kwargs.pop('pathMod') / self.filename.name

        # copy header for multiprocessing
        header_copy = copy(self.header)

        for key, value in kwargs.items():

            if key in header_copy.dtype.names:

                header_copy[key] = value

                with open(pathMod or self.filename, 'r+b') as f:

                    f.seek(0)

                    f.write(header_copy.tobytes())

                    # f.flush()

            else:

                print(f'{key} not in header')

        self.header = header_copy

    def scale_data(self,
                   index: int,
                   count: int,
                   o_min: int,
                   o_max: int,
                   n_min: int,
                   n_max: int,
                   pathMod: Path = None,
                   clamped: bool = False) -> None:
        """

        :param clamped:
        :param pathMod:
        :param n_max:
        :param n_min:
        :param o_max:
        :param o_min:
        :param count:
        :param index: object
        """

        o_min = int(o_min)
        o_max = int(o_max)
        n_min = int(n_min)
        n_max = int(n_max)


        if pathMod is not None:
            pathMod = pathMod / self.filename.name

        with open(pathMod or self.filename, 'r+b') as f:

            f.seek(self.header.itemsize + index * self.bytes)  # todo optional times 2 or times 8 dependant bytes

            sample = f.read(self.bytes * count)

            data = [int.from_bytes(sample[k:k + self.bytes], 'little') for k in range(0, len(sample), self.bytes)]

            scaled = scale(data, o_min, o_max, n_min, n_max).astype(int)


            # result = []
            #
            # for val in scaled.tolist():
            #
            #     check = val.to_bytes(self.bytes, 'little', signed=False)
            #
            #     result.append(check)

            result = [val.to_bytes(self.bytes, 'little', signed=False)
                      for val in scaled.tolist()]

            f.seek(self.header.itemsize + index * self.bytes)

            f.write(b''.join(result))

            f.flush()

        self.modHeader(EngZero=n_min,
                       EngFull=n_max,
                       RawZero=n_min,
                       RawFull=n_max)

    def byte_2_to_float(self,
                        pathMod: Path = None,
                        clamped: bool = False) -> None:
        """

        :param count:
        :type index: object
        """

        n_min = int(self.header['EngZero'])
        n_max = int(self.header['EngFull'])

        if pathMod is not None:
            pathMod = pathMod / self.filename.name

        with open(pathMod or self.filename, 'r+b') as f:

            f.seek(self.header.itemsize + 0 * self.bytes)  # todo optional times 2 or times 8 dependant bytes

            sample = f.read(self.bytes * self.header['dataLength'])

            data = [int.from_bytes(sample[k:k + self.bytes], 'little') for k in range(0, len(sample), self.bytes)]

            #scaled = [int(val) for val in scale_float(data, n_min, n_max)]
            scaled = scale_float(data, n_min, n_max)

            # result = []
            #
            # for val in scaled:
            #
            #     check = val.to_bytes(self.bytes, 'little', signed=True)
            #
            #     result.append(check)

            result = [val.to_bytes(self.bytes, 'little', signed=False)
                      for val in scaled.tolist()]

            f.seek(self.header.itemsize + 0 * self.bytes)

            f.write(b''.join(result))

            # if type(result) is not bytes:
            #
            #     #f.write(reduce(lambda x, y: x + y, result))
            #     #f.write(quick_reduce(np.array(result)))
            #     #f.write(quick_reduce(np.array(result)))
            #     f.write(b''.join(result))
            #
            # else:
            #
            #     f.write(result)

            f.flush()

        # change header

        # self.header.dtype = header_data(6)

        # x = np.array(list(self.header), dtype=header_data(6))

        blank = np.empty(1, dtype=header_data(6))

        blank["name"] = self.header["name"]
        blank["RawZero"] = self.header["RawZero"]
        blank["RawFull"] = self.header["RawFull"]
        blank["EngZero"] = self.header["EngZero"]
        blank["EngFull"] = self.header["EngFull"]
        blank["ID"] = self.header["ID"]
        blank["filetype"] = self.header["filetype"]
        blank["version"] = 6
        blank["startEvNo"] = self.header["startEvNo"]
        blank["logName"] = self.header["logName"]
        blank["mode"] = self.header["mode"]
        blank["area"] = self.header["area"]
        blank["priv"] = self.header["priv"]
        blank["hystoryType"] = self.header["hystoryType"]
        blank["samplePeriod"] = self.header["samplePeriod"]
        blank["sEngUnits"] = self.header["sEngUnits"]
        blank["format"] = self.header["format"]
        blank["startTime"] = self.header["startTime"] * 1E7 - 11644473600
        blank["endTime"] = self.header["endTime"] * 1E7 - 11644473600
        blank["dataLength"] = self.header["dataLength"]
        blank["filePointer"] = self.header["filePointer"]
        blank["endEvNo"] = self.header["endEvNo"]
        blank["alignment1"] = self.header["alignment1"]

        with open(pathMod or self.filename, 'rb') as file:
            contents = file.read()[self.header.itemsize:]

        with open(pathMod or self.filename, 'wb') as file:
            file.write(blank.tobytes())
            file.write(contents)

    def modMasterData(self):
        pass


@njit()
def quick_reduce_function(x, y):
    return x + y

@njit()
def quick_reduce(L):
    return reduce(quick_reduce_function, L)



if __name__ == '__main__':
    pass
