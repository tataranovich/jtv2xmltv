from datetime import datetime
from jtv2xmltv.utils import filetime_to_datetime


def test_filetime_to_datetime():
    ftime = b'\x00\xC0\xF9\x78\xB1\xEE\xD0\x01'
    dtime = datetime(2015, 9, 14, 5, 52)
    assert filetime_to_datetime(ftime) == dtime
