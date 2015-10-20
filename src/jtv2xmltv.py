# -*- coding: utf-8 -*-
# Copyright (c) 2015  Andrey Tataranovich <tataranovich@gmail.com>
# License: GPL-3
# Website: https://github.com/tataranovich/jtv2xmltv
import sys
import zipfile
import struct
import xml.etree.ElementTree as ET
import argparse
import datetime

reload(sys)
sys.setdefaultencoding('utf8')


def parse_titles(data):
    jtv_header = "JTV 3.x TV Program Data\x0a\x0a\x0a"
    if data[0:26] != jtv_header:
        raise Exception('Invalid JTV format')
    data = data[26:]
    titles = []
    while len(data) > 0:
        title_length = int(struct.unpack('<H', data[0:2])[0])
        data = data[2:]
        # TODO: epg titles encoding could be not cp1251
        title = data[0:title_length].decode('cp1251')
        data = data[title_length:]
        titles.append(title)
    return titles


def filetime_to_datetime(time):
    filetime = struct.unpack("<Q", time)[0]
    timestamp = filetime/10
    return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp)


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


def convert_jtv_to_xmltv(jtv_filename, xmltv_filename=None, epg_encoding="UTF-8", epg_timezone="UTC", epg_lang=None):
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
            xmltv_channel = ET.SubElement(xmltv_tv, 'channel', id=str(channel_id))
            if epg_lang is not None:
                ET.SubElement(xmltv_channel, 'display-name', lang=str(epg_lang)).text = channel_name
            else:
                ET.SubElement(xmltv_channel, 'display-name').text = channel_name
    channel_id = 0
    for filename in archive.namelist():
        if filename.endswith('.pdt'):
            channel_id = channel_id + 1
            titles = archive.read(filename)
            channel_titles = parse_titles(titles)
            schedules = archive.read(filename[0:-4] + ".ndx")
            channel_schedules = parse_schedule(schedules)

            i = 0
            for curr_title in channel_titles:
                if i < len(channel_schedules) - 1:
                    if epg_timezone != "UTC":
                        time_format = '%Y%m%d%H%M%S ' + epg_timezone
                    else:
                        time_format = '%Y%m%d%H%M%S'
                    xmltv_programme = ET.SubElement(xmltv_tv, 'programme',
                                                    start=channel_schedules[i].strftime(time_format),
                                                    stop=channel_schedules[i+1].strftime(time_format),
                                                    channel=str(channel_id))
                    if epg_lang is not None:
                        ET.SubElement(xmltv_programme, 'title', lang=str(epg_lang)).text = curr_title
                    else:
                        ET.SubElement(xmltv_programme, 'title').text = curr_title
                    i = i + 1
    if xmltv_filename is None or xmltv_filename == "-":
        print ET.tostring(xmltv_tv, encoding=epg_encoding, method="xml")
    else:
        xmltv = ET.ElementTree(xmltv_tv)
        xmltv.write(xmltv_filename, encoding=epg_encoding, xml_declaration=True)
    archive.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', required=True)
    parser.add_argument('-o', '--outputfile', default='-')
    parser.add_argument('-t', '--timezone')
    args = parser.parse_args()
    jtv_filename = args.inputfile
    xmltv_filename = args.outputfile
    if args.timezone is None:
        tz_format = 'UTC'
    elif args.timezone[0] == '-' or args.timezone[0] == '+':
        tz_format = str(args.timezone)
    else:
        tz_format = '+' + str(args.timezone)
    convert_jtv_to_xmltv(jtv_filename, xmltv_filename, epg_timezone=tz_format)


if __name__ == "__main__":
    main()
