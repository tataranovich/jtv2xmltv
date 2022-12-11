from __future__ import print_function
from xml.etree import ElementTree
import zipfile
import sys
from jtv2xmltv.parser import parse_schedule, is_valid_jtv, get_program_title
from jtv2xmltv.utils import fix_zip_filename


def convert_jtv_to_xmltv(jtv_filename, jtv_encoding="cp1251", xmltv_encoding="utf8", xmltv_timezone="UTC",
                         xmltv_lang=None):
    archive = zipfile.ZipFile(jtv_filename, 'r')
    xmltv_tv = ElementTree.Element('tv')
    channel_id = 0
    for filename in archive.namelist():
        if filename.endswith('.pdt'):
            unicode_name = fix_zip_filename(filename)
            channel_name = unicode_name[0:-4]
            channel_id = channel_id + 1
            xmltv_channel = ElementTree.SubElement(xmltv_tv, 'channel', id=str(channel_id))
            if xmltv_lang is not None:
                ElementTree.SubElement(xmltv_channel, 'display-name', lang=str(xmltv_lang)).text = channel_name
            else:
                ElementTree.SubElement(xmltv_channel, 'display-name').text = channel_name
    channel_id = 0
    for filename in archive.namelist():
        if filename.endswith('.ndx'):
            channel_id = channel_id + 1
            schedules_data = archive.read(filename)
            titles_filename = filename[0:-4] + ".pdt"
            titles_data = archive.read(titles_filename)
            try:
                if is_valid_jtv(titles_data):
                    channel_schedules = parse_schedule(schedules_data, titles_data, jtv_encoding)
                else:
                    print("Invalid JTV data in {}".format(titles_filename), file=sys.stderr)
            except Exception as e:
                print("Failed to parse {}: {}".format(filename, str(e)), file=sys.stderr)
                continue

            i = 0
            if xmltv_timezone != "UTC":
                time_format = '%Y%m%d%H%M%S ' + xmltv_timezone
            else:
                time_format = '%Y%m%d%H%M%S'
            while i < len(channel_schedules):
                if i < len(channel_schedules) - 1:
                    xmltv_programme = ElementTree.SubElement(xmltv_tv, 'programme',
                                                             channel=str(channel_id),
                                                             start=channel_schedules[i]['time'].strftime(time_format),
                                                             stop=channel_schedules[i+1]['time'].strftime(time_format)
                                                             )
                else:
                    xmltv_programme = ElementTree.SubElement(xmltv_tv, 'programme',
                                                             channel=str(channel_id),
                                                             start=channel_schedules[i]['time'].strftime(time_format)
                                                             )
                title = channel_schedules[i]['title']
                if xmltv_lang is not None:
                    ElementTree.SubElement(xmltv_programme, 'title', lang=str(xmltv_lang)).text = title
                else:
                    ElementTree.SubElement(xmltv_programme, 'title').text = title
                i = i + 1
    archive.close()
    return ElementTree.tostring(xmltv_tv, encoding=xmltv_encoding, method="xml").decode(encoding=xmltv_encoding)
