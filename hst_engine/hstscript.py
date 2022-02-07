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

class HSTScript:

    def __init__(self, hstslice, commands):

        self.hstslice = hstslice

        self.commands = commands

    def execute(self):

        for command in self.commands:


            getattr(self.hstslice, command[0])(*command[-1])


