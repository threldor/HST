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
def scale_fast(data: List, old_min: int, old_max: int, new_min: int, new_max: int):
    """fast scaling of a list of data between two ranges
    :param new_max:
    :param new_min:
    :param old_max:
    :param old_min:
    :param data: List
    """
    return [((d - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
            if d not in [-32001, -32002] else d
            for d in data]
    #todo(jaun) add the check here for valid/gated data


def scale(data, old_min, old_max, new_min, new_max):
    """

    :type data: object
    """
    if isinstance(data, list) or isinstance(data, List):

        return scale_fast(List(data), old_min, old_max, new_min, new_max)

    else:

        return ((data - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min

def scale_triple(data, min_1, max_1, min_2, max_2, min_3, max_3):
    """

    :type data: object
    """
    data_new = scale(data, min_1, max_1, min_2, max_2)

    print('intermediate:', data_new)

    return scale(data_new, min_2, max_2, min_3, max_3)

def scale_triple_single_call(data, min_1, max_1, min_3, max_3):
    """

    :type data: object
    """
    return [((min_3 - max_3)*(d - min_1)/(min_1 - max_1)) + min_3 for d in data]

if __name__ == '__main__':

    print(scale_triple([0, 5, 20, 50], 0, 100, -100, 100, 0, 1))

    print(scale_triple_single_call([0, 5, 20, 50], 0, 100, 0, 1))
