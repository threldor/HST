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
from HSTData import HSTData
from pathlib import Path


class HST(object):

    def __init__(self, filename: Path = None) -> None:

        self.HSTMaster = None

        self.HSTDataitems = []

        self.filename = None

        self.drive = None

        self.repath = None

        if filename is not None:

            self.load(filename)


    def load(self, filename: Path) -> None:

        self.filename = filename

        self.HSTMaster = HSTMaster(self, self.filename)

        self.HSTDataitems = [HSTData(self.HSTMaster, data) for data in self.HSTMaster.data]


if __name__ == '__main__':

    inputFile = Path('../resources/ST051DOS01FIT0780201acHi.HST')

    hst = HST()

    hst.drive = 'C'

    hst.repath = Path(r'C:\Users\jaun.vanheerden\PycharmProjects\HST\resources\converted')

    hst.load(inputFile)
