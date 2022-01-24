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
from formats import *
from HSTMaster import HSTMaster
from HSTHeader import HSTHeader
from pathlib import Path


class HST(object):

    def __init__(self, filename: Path = None) -> None:

        self.HSTMaster = None

        self.HSTHeaders = []

        self.filename = None

        if filename is not None:

            self.load(filename)


    def load(self, filename: Path) -> None:

        self.filename = filename

        self.HSTMaster = HSTMaster(self.filename)

        self.HSTHeaders = [HSTHeader(data) for data in self.HSTMaster.data]


if __name__ == '__main__':

    hst = HST()
