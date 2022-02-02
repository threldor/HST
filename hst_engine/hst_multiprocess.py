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
from hst import HST
import datetime
import json
import multiprocessing
from pathlib import Path
from multiprocessing import Pool
import tqdm
import time
from itertools import groupby


class HST_Multi:

    functions = {'MOD': 'modHeader',
                 'SCL': 'scale'}

    def __init__(self):
        self.scripts = []

    def run(self):
        with Pool(2) as p:
            tqdm.tqdm(p.imap(self.process, range(30)), total=30)

    def process(self):

        pass


    def csv_script(self, csv_file, repath: Path = None, drive: Path = None):

        with open(csv_file, 'r') as csv:

            for scriptLine in csv:

                filename, *timeslices = scriptLine.split(',?')

                print(filename)

                # create a HST object
                hst = HST(filename, repath, drive)

                for timeslice in timeslices:

                    timeSpan, *commands = timeslice.split(',$')  # todo whole file

                    startTime, endTime = map(lambda x: datetime.datetime.strptime(x, "%d/%m/%Y:%H:%M"),
                                             timeSpan.split(','))

                    print()

                    print(startTime, endTime)

                    print(*commands, sep='\n')

                    # create the slice

                    hstslice = hst[startTime:endTime]

                    for command in commands:

                        function, *args = command.split(',')

                        function = self.functions[function]

                        print(function, args)





# main
if __name__ == '__main__':

    hstm = HST_Multi()

    hstm.csv_script('C:/Users/jaun.vanheerden/PycharmProjects/HST/resources/script_test',
                    Path('C:/Users/jaun.vanheerden/PycharmProjects/HST/resources/converted/2-Byte'),
                    'C')
