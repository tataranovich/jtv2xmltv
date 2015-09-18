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

def dump_jtv_file(jtv_filename):
    archive = zipfile.ZipFile(jtv_filename, 'r')
    for filename in archive.namelist():
        if filename.endswith('.pdt'):
            try:
                unicode_name = filename.decode('UTF-8').encode('UTF-8')
            except:
                unicode_name = filename.decode('cp866').encode('UTF-8')
            channel_name = unicode_name[0:-4]
            titles = archive.read(filename)
            channel_titles = parse_titles(titles)
            schedules = archive.read(filename[0:-4] + ".ndx")
            channel_schedules = parse_schedule(schedules)

            print "****"
            print "**** ", channel_name
            print "****"

            i = 0
            prev_title = None
            curr_title = channel_schedules[i].strftime('%A, %d/%m/%Y')
            for title in channel_titles:
                if i < len(channel_schedules) - 1:
                    if curr_title != prev_title:
                        print ""
                        print curr_title
                        print ""
                        prev_title = curr_title
                    print channel_schedules[i].strftime('%H:%M'), "-", channel_schedules[i+1].strftime('%H:%M'), title
                    curr_title = channel_schedules[i].strftime('%A, %d/%m/%Y')
                i = i + 1
            print ""

filename = sys.argv[1]

dump_jtv_file(filename)

