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
from pprint import pprint
from pathlib import Path
import numpy as np


class HSTMaster(object):


    def __init__(self, parent, filename: Path) -> None:
        """

        :type filename: Path
        """

        self.parent = parent

        self.dt_header = np.dtype(MASTER_H)

        self.header = np.fromfile(filename, dtype=self.dt_header, count=1)[0]

        self.dt_data = np.dtype(header_HST(self.header['version']))

        self.data = np.fromfile(filename,
                                dtype=self.dt_data,
                                count=self.header['nFiles'],
                                offset=self.dt_header.itemsize)

        # set the data segment and data length (choose first) # todo check no inconsistencies
        self.dataLengthSegment = self.data['dataLength'][0]

        self.dataLength = self.dataLengthSegment * len(self.data['dataLength'])


    def __len__(self) -> int:

        return len(self.data)


    def __getitem__(self, key: str):

        return self.header[key]


if __name__ == '__main__':

    inputFile = Path("../resources/converted/ST051DOS01FIT0780201acHi.HST")

    hst_master = HSTMaster(inputFile)

