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
from formats import header_HST
from pathlib import Path
import numpy as np
from hst_engine import HSTMaster
from utils.str_conversion import bytes_to_str
from pprint import pprint


class HSTData(object):

    def __init__(self, master: HSTMaster, data: np.void) -> None:

        self.master = master

        self.dt_header = header_HST(master['version'])

        self.filename = bytes_to_str(master['filename'])

        # read the HST and push to dict
        self._header_raw = np.fromfile(self.filename, dtype=self.dt_header, count=1)[0]

        self.header = dict(zip(self._header_raw.dtype.names, self._header_raw))

        pprint(self.header)



if __name__ == '__main__':

    hst_header = HSTData()
