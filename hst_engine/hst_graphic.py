import numpy as np
import pyqtgraph as pg


# imports

from pathlib import Path
from hst import HST
import datetime

# setup the input file pointing to the HST_one file (master)
inputFile = Path(r'../resources/converted/2-Byte/ST051DOS01FIT0780201acHi.HST')

# create a blank HST_one object to set the drive prior to loading
hst = HST()

hst.drive = 'C'

# repath to the following dir, this repath replaces the paths
# within the HST_one
hst.repath = Path(r'../resources/converted/2-Byte')

# load
hst.load(inputFile)

# <single file editing>
# choose object
HST_10 = hst.HSTDataItems[10]

# setup a time span
start = datetime.datetime(2020, 12, 12, 0, 1, 0)

end = datetime.datetime(2021, 12, 12, 0, 4, 0)

# create a slice, very easy non-inclusive end
# this can also be indexes based from the oldest file start
# as the offset start - negative indexes allowed
slice_dt = hst[start:end]

#data = np.random.normal(size=1000)
data_x, data_y = slice_dt.get_data()

pg.plot(data_x, data_y, title="Simplest possible plotting example")

# data = np.random.normal(size=(500,500))
# pg.image(data, title="Simplest possible image example")

if __name__ == '__main__':
    pg.exec()
