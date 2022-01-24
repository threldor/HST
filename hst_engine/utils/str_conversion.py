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


def bytes_to_str(bytes_input: bytes, encoding: str = 'ASCII') -> str:
    """x
    :param encoding:
    :type bytes_input: bytes
    """
    return bytes_input.decode(encoding).strip().strip('\x00').replace('\\', '/')


if __name__ == '__main__':
    print(bytes_to_str(b'this is a \x03 byte'))

    pass
