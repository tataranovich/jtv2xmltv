import struct
from jtv2xmltv.utils import filetime_to_datetime


def is_valid_jtv(data):
    jtv_headers = [b"JTV 3.x TV Program Data\x0a\x0a\x0a", b"JTV 3.x TV Program Data\xa0\xa0\xa0"]
    return data[0:26] in jtv_headers


def get_program_title(data, offset, encoding="cp1251"):
    title_length = int(struct.unpack('<H', data[offset:offset+2])[0])
    return data[offset+2:offset+2+title_length].decode(encoding)


def parse_schedule(ndx_data, pdt_data, encoding="cp1251"):
    schedules = []
    records_num = struct.unpack('<H', ndx_data[0:2])[0]
    ndx_data = ndx_data[2:]
    i = 0
    while i < records_num:
        i = i + 1
        record = ndx_data[0:12]
        ndx_data = ndx_data[12:]
        program = {}
        program["time"] = filetime_to_datetime(record[2:-2])
        offset = struct.unpack('<H', record[-2:])[0]
        program["title"] = get_program_title(pdt_data, offset, encoding)
        schedules.append(program)
    return schedules
