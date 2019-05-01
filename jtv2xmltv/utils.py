import datetime
import struct
import sys


def filetime_to_datetime(time):
    filetime = struct.unpack("<Q", time)[0]
    timestamp = filetime / 10
    return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp)


def fix_zip_filename_python2(filename):
    try:
        unicode_name = filename.decode('UTF-8').encode('UTF-8')
    except UnicodeDecodeError:
        unicode_name = filename.decode('cp866').encode('UTF-8')
    return unicode_name


def fix_zip_filename_python3(filename):
    try:
        unicode_name = str(bytes(filename, encoding='cp437'), encoding='cp866')
    except UnicodeEncodeError:
        unicode_name = filename
    return unicode_name


def fix_zip_filename(filename):
    if int(sys.version[0]) == 2:
        return fix_zip_filename_python2(filename)
    else:
        return fix_zip_filename_python3(filename)
