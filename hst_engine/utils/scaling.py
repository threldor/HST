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
from numba import jit
from numba.typed import List


@jit(nopython=True)
def scale_fast(data, old_min, old_max, new_min, new_max):
    return [((d - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min for d in data]
    #todo(jaun) add the check here for valid/gated data


def scale(data, old_min, old_max, new_min, new_max):
    return scale_fast(List(data), old_min, old_max, new_min, new_max)
