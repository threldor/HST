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
from HSTMaster import HSTMaster
from utils.str_conversion import bytes_to_str
from pprint import pprint
import os


class HSTData(object):

    def __init__(self,
                 master: HSTMaster,
                 data: np.void) -> None:

        self.master = master

        self.dt_header = header_HST(master['version'])

        self.filename = Path(bytes_to_str(data['name']))

        self._header_raw = None

        self.header = None


        self.load()


    def load(self):

        # read the HST and push to dict
        try:
            
            _filename = self.filename
            
            if self.master.parent.drive is not None:

                _filename = Path(f"{self.master.parent.drive}:{os.path.splitdrive(_filename)[-1]}")

            if self.master.parent.repath is not None:

                _filename = self.master.parent.repath / _filename.name

            self._header_raw = np.fromfile(_filename, dtype=self.dt_header, count=1)[0]

        except FileNotFoundError as e:

            print(e)

        if self._header_raw is not None:

            self.header = dict(zip(self._header_raw.dtype.names, self._header_raw))

            pprint(self.header)



if __name__ == '__main__':

    hst_header = HSTData()
