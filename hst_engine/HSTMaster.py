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

from utils.str_conversion import byte_to_str


class HSTMaster(object):

    def __init__(self, filename: Path):
        """

        :type filename: Path
        """
        self.dt_header = np.dtype(MASTER_H)

        # read the HST and push to dict
        self._data_raw = np.fromfile(filename, dtype=self.dt_header, count=1)[0]

        self.header = dict(zip(self._data_raw.dtype.names, self._data_raw))

        self.dt_data = np.dtype(header_HST(self.header['version']))

        self.data = np.fromfile(inputFile,
                                dtype=self.dt_data,
                                count=self.header['nFiles'],
                                offset=self.dt_header.itemsize)

        pprint(self.data)
        print('----')
        print(self.data[0])
        print(type(self.data[0]))

        # # pprint(self.data)
        # HSTHdt = np.dtype(HSTHeader(version))
        # # read the HST data array and push to dict, offset by master header
        # f = np.fromfile(inputFile, dtype=HSTHdt, count=nFiles, offset=HSTMdt.itemsize)

    def __len__(self):
        return len(self.data)

    # def __repr__(self):
    #     return pprint(self.data)
    #
    # def __str__(self):
    #     return self.name


if __name__ == '__main__':
    inputFile = Path("../resources/converted/ST051DOS01FIT0780201acHi.HST")

    hst_master = HSTMaster(inputFile)
