import struct
from jtv2xmltv.utils import filetime_to_datetime


def parse_titles(data, encoding="cp1251"):
    jtv_headers = [b"JTV 3.x TV Program Data\x0a\x0a\x0a", b"JTV 3.x TV Program Data\xa0\xa0\xa0"]
    if data[0:26] not in jtv_headers:
        raise Exception('Invalid JTV format')
    data = data[26:]
    titles = []
    while data:
        title_length = int(struct.unpack('<H', data[0:2])[0])
        data = data[2:]
        title = data[0:title_length].decode(encoding)
        data = data[title_length:]
        titles.append(title)
    return titles


def parse_schedule(data):
    schedules = []
    records_num = struct.unpack('<H', data[0:2])[0]
    data = data[2:]
    i = 0
    while i < records_num:
        i = i + 1
        record = data[0:12]
        data = data[12:]
        schedules.append(filetime_to_datetime(record[2:-2]))
    return schedules
