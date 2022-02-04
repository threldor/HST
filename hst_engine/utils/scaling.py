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


@jit(nopython=True)
def scale_fast_2_byte(data: List, old_min: int, old_max: int, new_min: int, new_max: int, inval: bool = True):
    # if (d < 0 or d > 32_000) and inval:
    #
    #     if d < 0:
    #         d = 0
    #
    #     else:
    #
    #
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

        return scale_fast_2_byte(List(data), old_min, old_max, new_min, new_max)

    else:

        return ((data - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min


def scale_float(data, old_min, old_max, new_min, new_max):
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
    return [((min_3 - max_3) * (d - min_1) / (min_1 - max_1)) + min_3 for d in data]


if __name__ == '__main__':
    # print(scale_triple([0, 5, 20, 50], 0, 100, -100, 100, 0, 1))
    #
    # print(scale_triple_single_call([0, 5, 20, 50], 0, 100, 0, 1))

    # test

    val = 12800

    e_old_min, e_old_max = 0, 500

    e_new_min, e_new_max = 0, 1000

    scale_min, scale_max = 0, 32000

    # scale to eng
    val_e_old = scale(val, scale_min, scale_max, e_old_min, e_old_max)

    # scale to scale
    val_final = scale(val_e_old, e_new_min, e_new_max, scale_min, scale_max)

    print(f'val:\t{val}\n'
          f'engineer old:\t{e_old_min}-{e_old_max}\n'
          f'\nscale:\t{scale_min}-{scale_max}')

    print()
    print('\t|\t'.join(['val    ', 'val_e_o', 'val_final']))
    print('\t->\t'.join([str(round(i, 2)) for i in [val, val_e_old, val_final]]))
