from xml.etree import ElementTree
import zipfile
import sys
from jtv2xmltv.parser import parse_schedule, parse_titles
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
        if filename.endswith('.pdt'):
            channel_id = channel_id + 1
            try:
                titles_filename = filename
                titles = archive.read(titles_filename)
                channel_titles = parse_titles(titles, encoding=jtv_encoding)
            except Exception:
                print("Failed to process titles in {}".format(titles_filename))
                continue

            try:
                schedules_filename = filename[0:-4] + ".ndx"
                schedules = archive.read(schedules_filename)
                channel_schedules = parse_schedule(schedules)
            except Exception:
                print("Failed to process schedule in {}".format(schedules_filename))
                continue

            i = 0
            for curr_title in channel_titles:
                if xmltv_timezone != "UTC":
                    time_format = '%Y%m%d%H%M%S ' + xmltv_timezone
                else:
                    time_format = '%Y%m%d%H%M%S'
                if i < len(channel_schedules) - 1:
                    xmltv_programme = ElementTree.SubElement(xmltv_tv, 'programme',
                                                             start=channel_schedules[i].strftime(time_format),
                                                             stop=channel_schedules[i+1].strftime(time_format),
                                                             channel=str(channel_id))
                else:
                    xmltv_programme = ElementTree.SubElement(xmltv_tv, 'programme',
                                                             start=channel_schedules[i].strftime(time_format),
                                                             channel=str(channel_id))
                if xmltv_lang is not None:
                    ElementTree.SubElement(xmltv_programme, 'title', lang=str(xmltv_lang)).text = curr_title
                else:
                    ElementTree.SubElement(xmltv_programme, 'title').text = curr_title
                i = i + 1
    archive.close()
    return ElementTree.tostring(xmltv_tv, encoding=xmltv_encoding, method="xml").decode(encoding=xmltv_encoding)
