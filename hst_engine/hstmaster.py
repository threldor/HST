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
from formats import MASTER_H, header_HST
import datetime
from pathlib import Path
import numpy as np
import os
from copy import copy


class HSTMaster(object):
    """

    """

    def __init__(self, parent, filename: Path) -> None:
        """

        :type filename: Path
        """

        self.parent = parent

        self.filename = Path(os.path.abspath(filename))

        self.dt_header = np.dtype(MASTER_H)

        self.header = np.fromfile(self.filename,
                                  dtype=self.dt_header,
                                  count=1)[0]

        self.dt_data = np.dtype(header_HST(self.header['version']))

        self.data_original = np.fromfile(self.filename,
                                dtype=self.dt_data,
                                count=self.header['nFiles'],
                                offset=self.dt_header.itemsize)

        self.data = self.data_original[np.apply_along_axis(lambda x: x['startTime'],
                                                  axis=0,
                                                  arr=self.data_original).argsort()]

        self.data_index = np.apply_along_axis(lambda x: x['startTime'],
                                              axis=0,
                                              arr=self.data).argsort()

        # set the data segment and data length (choose first) # todo check no inconsistencies
        self.dataLengthSegment = self.data['dataLength'][0]

        self.dataLength = self.dataLengthSegment * len(self.data['dataLength'])

        self.filePointerRef = np.where(self.data['startTime'] == max(self.data['startTime']))

        self.filePointer = self.data[self.filePointerRef]['filePointer']

        self.samplePeriod = int(self.data['samplePeriod'][0] / 1000)


        try:
            # 2 byte
            self.earliest = datetime.datetime.utcfromtimestamp(min(self.data['startTime']))

        except:
            # 8 byte
            self.earliest = datetime.datetime.utcfromtimestamp(int((min(self.data['startTime']) / 1E7)) - 11_644_473_600)

        try:
            # 2 byte
            self.latest = datetime.datetime.utcfromtimestamp(max(self.data['endTime']))

        except:
            # 8 byte
            self.latest = datetime.datetime.utcfromtimestamp(int((max(self.data['endTime']) / 1E7)) - 11_644_473_600)


    def __len__(self) -> int:

        return len(self.data)

    def __getitem__(self, key: str):

        return self.header[key]



    def modHSTHeader(self, *args, **kwargs: dict) -> None:
        """

        :param args:
        :param kwargs:
        :return:
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

        for key, value in kwargs.items():

            if key in self.header.dtype.names:

                self.header[key] = value

        with open(pathMod or self.filename, 'r+b') as f:

            f.seek(0)

            f.write(self.header.tobytes())


    def modHSTDataItems(self, *args, **kwargs: dict) -> None:
        """

        :param args:
        :param kwargs:
        :return:
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

        with open(pathMod or self.filename, 'r+b') as f:

            f.seek(self.header.itemsize)

            buffer = b''

            for index, data in enumerate(self.data_original[::-1]):

                for key, value in kwargs.items():

                    if key in data.dtype.names:
                        data[key] = value

                buffer += data.tobytes()

            f.write(buffer)

            # f.flush()

    def modHSTDataItem(self, index: int, *args, **kwargs: dict) -> None:
        """

        :param index:
        :param args:
        :param kwargs:
        :return:
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
        HSTDataItem_copy = copy(self.data_original[index])

        for key, value in kwargs.items():

            if key in HSTDataItem_copy.dtype.names:

                HSTDataItem_copy[key] = value

                with open(pathMod or self.filename, 'r+b') as f:

                    f.seek(self.header.itemsize + (index * HSTDataItem_copy.itemsize))

                    f.write(HSTDataItem_copy.tobytes())

                    # f.flush()

            else:

                print(f'{key} not in header')


if __name__ == '__main__':
    pass
