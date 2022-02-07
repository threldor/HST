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
from multiprocessing import Pool, cpu_count, freeze_support
import tqdm
import time
from hstscript import HSTScript
from itertools import groupby


class HST_Multi:
    functions = {'MOD': 'modHeader',
                 'SCL': 'scale',
                 'B2F': 'to_float',
                 'OFS': 'offsetTime',
                 'OFST': 'offsetToToday',
                 'MOD_MAST_H': 'modMasterHST',
                 'MOD_MAST_D': 'modMasterHSTDataItem',
                 'MOD_MAST_D+': 'modMasterHSTDataItems'}

    def __init__(self):
        self.HSTs = []

    def run(self):
        with Pool(cpu_count()) as p:
            tqdm.tqdm(p.map(process, self.HSTs), total=len(self.HSTs))

    def csv_script(self, csv_file, repath: Path = None, drive: str = None):

        with open(csv_file, 'r') as csv:

            for scriptLine in csv:

                hst_group = []

                filename, *timeslices = [line.strip() for line in scriptLine.split(',?')]

                # create a HST object
                hst = HST(filename, repath, drive)

                for timeslice in timeslices:

                    timeSpan, *commands_s = timeslice.split(',$')  # todo whole file

                    startTime, endTime = map(lambda x: datetime.datetime.strptime(x, "%d/%m/%Y:%H:%M"),
                                             timeSpan.split(','))

                    # create the slice

                    hstslice = hst[startTime:endTime]

                    commands = []

                    for command_s in commands_s:
                        function, *args = command_s.split(',')

                        function = self.functions[function]

                        print(function, args)

                        args = [dict([arg.split('=')]) if '=' in arg else arg for arg in args]

                        commands.append((function, args))

                    hst_group.append(HSTScript(hstslice, commands))

                self.HSTs.append(hst_group)


def process(hst):
    for script in hst:
        script.execute()


# main
if __name__ == '__main__':
    freeze_support()

    hstm = HST_Multi()

    hstm.csv_script('C:/Users/jaun.vanheerden/PycharmProjects/HST/hst_engine/script_test',
                    Path('C:/Users/jaun.vanheerden/PycharmProjects/HST/resources/converted/2-Byte'),
                    'C')

    # for script in hstm.scripts:
    #
    #     script.execute()

    hstm.run()
