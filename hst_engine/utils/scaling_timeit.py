import timeit



# compute binary search time
def scale_fast_2_byte():
    SETUP_CODE = '''
from scaling import scale_fast_2_byte
from random import choices
from numba.typed import List'''

    TEST_CODE = '''
scale_fast_2_byte(List(choices(range(0, 1_000), k=1_000)), 0, 1_000, 0, 100)'''

    # timeit.repeat statement
    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=3,
                          number=10000)

    # printing minimum exec. time
    print('scale_fast_2_byte: {}'.format(min(times)))


# compute linear search time
def scale_fast_2_byte_faster():
    SETUP_CODE = '''
from scaling import scale_fast_2_byte_faster
from random import choices
from numba.typed import List'''

    TEST_CODE = '''
scale_fast_2_byte_faster(List(choices(range(0, 1_000), k=1_000)), 0, 1_000, 0, 100)
    '''
    # timeit.repeat statement
    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=3,
                          number=10000)

    # printing minimum exec. time
    print('scale_fast_2_byte_faster: {}'.format(min(times)))

# compute linear search time
def scale_fast_2_byte_listcomp():
    SETUP_CODE = '''
from scaling import scale_fast_2_byte_listcomp
from random import choices
from numba.typed import List'''

    TEST_CODE = '''
scale_fast_2_byte_listcomp(List(choices(range(0, 1_000), k=1_000)), 0, 1_000, 0, 100)
    '''
    # timeit.repeat statement
    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=3,
                          number=1000)

    # printing minimum exec. time
    print('scale_fast_2_byte_listcomp: {}'.format(min(times)))

# compute linear search time
def scale_fast_2_byte_listcomp_slow():
    SETUP_CODE = '''
from scaling import scale_fast_2_byte_listcomp_slow
from random import choices
from numba.typed import List'''

    TEST_CODE = '''
scale_fast_2_byte_listcomp_slow(List(choices(range(0, 1_000), k=1_000)), 0, 1_000, 0, 100)
    '''
    # timeit.repeat statement
    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=3,
                          number=1000)

    # printing minimum exec. time
    print('scale_fast_2_byte_listcomp_slow: {}'.format(min(times)))


if __name__ == "__main__":
    #scale_fast_2_byte()
    #scale_fast_2_byte_faster()
    scale_fast_2_byte_listcomp()
    scale_fast_2_byte_listcomp_slow()