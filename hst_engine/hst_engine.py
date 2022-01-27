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
from pathlib import Path
from HST import HST
from numba.typed import List
from utils.scaling import scale


# main

if __name__ == '__main__':
    inputFile = Path('../resources/ST051DOS01FIT0780201acHi.HST')

    hst = HST()

    hst.drive = 'C'

    hst.repath = Path(r'C:\Users\jaun.vanheerden\PycharmProjects\HST\resources\converted')

    hst.load(inputFile)

    print(hst[1])
    print(hst[20160])
    print(hst[20161])

    hst.get_data(20160, 20160 * 3 + 5)

    print(scale(List(list(range(0, 1000, 2))), 0, 1000, -100, 100))
