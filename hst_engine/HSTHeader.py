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
from pathlib import Path
import numpy as np


class HSTHeader(object):

    def __init__(self, data: np.void = None) -> None:


        if data is not None:
            pass


if __name__ == '__main__':

    hst_header = HSTHeader()
