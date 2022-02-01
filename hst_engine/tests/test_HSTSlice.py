from hst_engine.hst import HST_one
import pytest
from pathlib import Path
import os
import sys
import datetime

# MACROS
path = Path(__file__).parent

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    path = Path(sys._MEIPASS)  # pylint: disable=no-member
path = os.path.dirname(os.path.realpath(__file__))
cwd = Path.cwd()

def test_HSTSlice_len():
    inputFile = Path('../resources/ST051DOS01FIT0780201acHi.HST_one')
    hst = HST_one()
    hst.drive = 'C'
    hst.repath = Path(r'C:\Users\jaun.vanheerden\PycharmProjects\HST\resources\converted')
    hst.load(inputFile)

    # setup datetime
    start = datetime.datetime(2020, 12, 12, 0, 1, 0)
    end = datetime.datetime(2021, 12, 12, 0, 4, 0)

    slice_dt = hst[start:end]
    print(len(slice_dt))

    #assert len(slice_dt) ==