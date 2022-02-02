import numpy as np
import pyqtgraph as pg


# imports

from pathlib import Path
from hst import HST
import datetime


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        return [datetime.datetime.utcfromtimestamp(3445345).strftime("%D: %H:%M") for value in values]

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

view = pg.plot(data_x, title="Simplest possible plotting example")

view.plotItem.axes['bottom'] = TimeAxisItem(orientation='bottom')

item = pg.InfiniteLine(movable=True)

view.addItem(item)

view.update()

if __name__ == '__main__':
    pg.exec()
