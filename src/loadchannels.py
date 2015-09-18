#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import zipfile
import struct
import filetimes

reload(sys)
sys.setdefaultencoding('utf8')

def parse_titles(data):
    jtv_header = "JTV 3.x TV Program Data\x0a\x0a\x0a"
    if data[0:26] != jtv_header:
        raise Exception('Invalid JTV format')
    data = data[26:]
    titles = []
    while len(data) > 0:
        title_length = int(struct.unpack('H', data[0:2])[0])
        data = data[2:]
        title = data[0:title_length].decode('cp1251')
        data = data[title_length:]
        titles.append(title)
    return titles

def parse_schedule(data):
    schedules = []
    records_num = struct.unpack('H', data[0:2])[0]
    data = data[2:]
    i = 0
    while i < records_num:
        i = i + 1
        record = data[0:12]
        data = data[12:]
        schedules.append(filetimes.filetime_to_dt(struct.unpack('<Q', record[2:-2])[0]))
    return schedules

filename = sys.argv[1]

archive = zipfile.ZipFile(filename, 'r')

for filename in archive.namelist():
    if filename.endswith('.pdt'):
        try:
            unicode_name = filename.decode('UTF-8').encode('UTF-8')
        except:
            unicode_name = filename.decode('cp866').encode('UTF-8')
        channel_name = unicode_name[0:-4]
        titles = archive.read(filename)
        channel_titles = parse_titles(titles)
        schedule = archive.read(filename[0:-4] + ".ndx")
        channel_schedule = parse_schedule(schedule)
        print " **** ", channel_name, " **** "
        j = 0
        for title in channel_titles:
            print channel_schedule[j], title
            j = j + 1