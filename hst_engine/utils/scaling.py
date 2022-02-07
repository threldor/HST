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
from numba import njit, jit, prange
from numba.typed import List
import numpy as np


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
            if d not in [33535, 33534] else d  #-32001 is 33535 and -32002 is 33534
            for d in data]



# @njit(fastmath=True)
@njit(parallel=True)
def scale_fast_2_byte_faster(data: np.array, old_min: int, old_max: int, new_min: int, new_max: int, inval: bool = True):

    y = np.empty(data.shape)

    for i in prange(len(data)):

        if data[i] in [33_535, 33_534]:

            y[i] = data[i]

        else:

            scaled = (old_min * (data[i] - 32_000) - old_max * data[i] + 32_000 * new_min) / (new_min - new_max)

            if scaled < 0 or scaled > 32_000:
                if inval:
                    # return 33_535
                    y[i] = 33_535
                else:
                    # return 0 if scaled < 0 else 32_000
                    y[i] = 0 if scaled < 0 else 32_000
            else:
                y[i] = scaled

    return y



@njit()
def scale_fast_2_byte_listcomp(data: List, old_min: int, old_max: int, new_min: int, new_max: int, inval: bool = True):

    return [(old_min * (d - 32_000) - old_max * d + 32_000 * new_min) / (new_min - new_max) for d in data]

def scale_fast_2_byte_listcomp_slow(data: List, old_min: int, old_max: int, new_min: int, new_max: int,
                               inval: bool = True):
    return [(old_min * (d - 32_000) - old_max * d + 32_000 * new_min) / (new_min - new_max) for d in data]


@jit(nopython=True)
def scale_fast_2_byte(data: List, old_min: int, old_max: int, new_min: int, new_max: int, inval: bool = True):

    result = []

    for d in data:

        if d in [33_535, 33_534]:

            #return d
            result.append(d)
            continue

        scaled = (old_min * (d - 32_000) - old_max * d + 32_000 * new_min) / (new_min - new_max)

        if scaled < 0 or scaled > 32_000:
            if inval:
                # return 33_535
                result.append(33_535)
                continue
            else:
                # return 0 if scaled < 0 else 32_000
                result.append(0 if scaled < 0 else 32_000)
                continue

        #return scaled
        result.append(scaled)

    return result

    # return [(old_min * (d - 32_000) - old_max * d + 32_000 * new_min) / (new_min - new_max)
    #
    #         if (d < 0 or d > 32_000) and not inval else (0 if d < 0 else 32_000)
    #
    # if d not in [33535, 33534] else d
    #         for d in data]


def scale(data, old_min, old_max, new_min, new_max):
    """

    :type data: object
    """
    if isinstance(data, list) or isinstance(data, List):

        #return scale_fast_2_byte(List(data), old_min, old_max, new_min, new_max)
        return scale_fast_2_byte_faster(np.array(data), old_min, old_max, new_min, new_max)

    else:

        return ((data - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min


def scale_float(data, new_min, new_max):
    """

    :type data: object
    """
    if isinstance(data, list) or isinstance(data, List):

        return scale_fast(List(data), 0, 32_000, new_min, new_max)

    else:

        return ((data - 0) / (32_000 - 0)) * (new_max - new_min) + new_min


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
    return [((min_3 - max_3) * (d - min_1) / (min_1 - max_1)) + min_3 for d in data]


if __name__ == '__main__':

    # test

    val = 12800

    e_old_min, e_old_max = 0, 500

    e_new_min, e_new_max = 0, 1000

    scale_min, scale_max = 0, 32000


    # timeit


