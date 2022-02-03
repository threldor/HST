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


class HSTMaster(object):

    def __init__(self, parent, filename: Path) -> None:
        """

        :type filename: Path
        """

        self.parent = parent

        self.filename = Path(os.path.abspath(filename))

        self.dt_header = np.dtype(MASTER_H)

        self.header = np.fromfile(self.filename, dtype=self.dt_header, count=1)[0]

        self.dt_data = np.dtype(header_HST(self.header['version']))

        self.data = np.fromfile(self.filename,
                                dtype=self.dt_data,
                                count=self.header['nFiles'],
                                offset=self.dt_header.itemsize)

        self.data = self.data[np.apply_along_axis(lambda x: x['startTime'], axis=0, arr=self.data).argsort()]

        # set the data segment and data length (choose first) # todo check no inconsistencies
        self.dataLengthSegment = self.data['dataLength'][0]

        self.dataLength = self.dataLengthSegment * len(self.data['dataLength'])

        self.filePointerRef = np.where(self.data['startTime'] == max(self.data['startTime']))

        self.filePointer = self.data[self.filePointerRef]['filePointer']

        self.samplePeriod = int(self.data['samplePeriod'][0]/1000)

        try:

            self.earliest = datetime.datetime.utcfromtimestamp(min(self.data['startTime']))

        except:

            self.earliest = datetime.datetime.utcfromtimestamp(int(min(self.data['startTime'])/100000000))


    def __len__(self) -> int:

        return len(self.data)

    def __getitem__(self, key: str):

        return self.header[key]


if __name__ == '__main__':

    pass
