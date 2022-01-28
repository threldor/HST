""""Jaun van Heerden
X.
Example:
    $ python hst_engine.py
"""

__author__ = __maintainer__ = ["Jaun van Heerden"]
__version__ = "1.0.0"
__email__ = ["jaun.vanheerden@allianceautomation.com.au"]
__status__ = "Production"

# statics

# float invalid and gated
INVALID_DATA_8_HEX = bytearray.fromhex("bbbbffffbbbbffff")
GATED_DATA_8_HEX = bytearray.fromhex("aaaaffffaaaaffff")
