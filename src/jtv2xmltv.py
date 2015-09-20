# -*- coding: utf-8 -*-
# Copyright (c) 2015  Andrey Tataranovich <tataranovich@gmail.com>
# License: GPL-3
# Website: https://github.com/tataranovich/jtv2xmltv
import sys
import zipfile
import struct
import filetimes
import xml.etree.ElementTree as ET

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

def convert_jtv_to_xmltv(jtv_filename, xmltv_filename, encoding="UTF-8", timezone="UTC"):
    archive = zipfile.ZipFile(jtv_filename, 'r')
    xmltv_tv = ET.Element('tv')
    channel_id = 0
    for filename in archive.namelist():
        if filename.endswith('.pdt'):
            try:
                unicode_name = filename.decode('UTF-8').encode('UTF-8')
            except:
                unicode_name = filename.decode('cp866').encode('UTF-8')
            channel_name = unicode_name[0:-4]
            channel_id = channel_id + 1
            xmltv_channel = ET.SubElement(xmltv_tv, 'channel', id = str(channel_id))
            ET.SubElement(xmltv_channel, 'display-name', lang="ru").text = channel_name
    channel_id = 0
    for filename in archive.namelist():
        if filename.endswith('.pdt'):
            try:
                unicode_name = filename.decode('UTF-8').encode('UTF-8')
            except:
                unicode_name = filename.decode('cp866').encode('UTF-8')
            channel_name = unicode_name[0:-4]
            channel_id = channel_id + 1
            titles = archive.read(filename)
            channel_titles = parse_titles(titles)
            schedules = archive.read(filename[0:-4] + ".ndx")
            channel_schedules = parse_schedule(schedules)

            i = 0
            for curr_title in channel_titles:
                if i < len(channel_schedules) - 1:
                    if timezone != "UTC":
                        time_format = '%Y%m%d%H%M%S ' + timezone
                    else:
                        time_format = '%Y%m%d%H%M%S'
                    xmltv_programme = ET.SubElement(xmltv_tv, 'programme', start=channel_schedules[i].strftime(time_format), stop=channel_schedules[i+1].strftime(time_format), channel = str(channel_id))
                    ET.SubElement(xmltv_programme, 'title', lang="ru").text = curr_title
                    i = i + 1
    xmltv = ET.ElementTree(xmltv_tv)
    xmltv.write(xmltv_filename, encoding='UTF-8', xml_declaration=True)

if __name__ == "__main__":
    jtv_filename = sys.argv[1]
    xmltv_filename = sys.argv[2]
    convert_jtv_to_xmltv(jtv_filename, xmltv_filename, timezone="+0300")

