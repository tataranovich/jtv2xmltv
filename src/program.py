# -*- coding: utf-8 -*-
import struct
import datetime
import sys
import zipfile
import xml.etree.ElementTree as et
import argparse


reload(sys)
sys.setdefaultencoding('utf8')

def filetime_to_datetime (time):
    filetime = struct.unpack("<Q", time)
    timestamp = filetime[0]/10
    return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp);


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfile', required = True)
parser.add_argument('-o', '--outputfile', default='-')
parser.add_argument('-t', '--timezone')
args = parser.parse_args()

filename = args.inputfile
archive = zipfile.ZipFile(filename, 'r')
idtv=0
top = et.Element('tv')
for filename in archive.namelist():
    if filename.endswith('.pdt'):
        try:
            unicode_name = filename.decode('UTF-8').encode('UTF-8')
        except:
            unicode_name = filename.decode('cp866').encode('UTF-8')
        idtv=idtv+1
        channel_name = unicode_name[0:-4]
        channelEl = et.SubElement(top, 'channel', id=str(idtv))
        display_name = et.SubElement(channelEl, 'display-name')
        display_name.text = channel_name
        ndxfile_name = filename[0:-4] + ".ndx"
        pdtfile_name = filename
        pdtfile = archive.open(pdtfile_name, 'r')
        pdt_data = pdtfile.read()
        if pdt_data[0:26]!= "JTV 3.x TV Program Data\x0A\x0A\x0A":
            raise BaseException("incorrect file")
        ndxfile = archive.open(ndxfile_name, 'r')
        ndx_data=ndxfile.read()
        recnum = ndx_data[0:2]
        ndx_data = ndx_data[2:]
        recordnum = struct.unpack("<H", recnum)[0]
        for i in range(0, recordnum):
            timestart = ndx_data[2:10]
            starttime = filetime_to_datetime(timestart)
            if i<> recordnum-1:
                timestop = ndx_data[14:22]
                stoptime = filetime_to_datetime(timestop)
            pdt = ndx_data[10:12]
            pdtindex = struct.unpack("<H", pdt)
            pdt_title_offset=pdtindex[0]
            Amt = pdt_data[pdt_title_offset:pdt_title_offset+2]
            Amount = struct.unpack("<H", Amt)
            name = pdt_data[pdt_title_offset+2:pdt_title_offset+2+Amount[0]]
            unicode_name = name.decode('cp1251').encode('UTF-8')
            if args.timezone is None:
                tz_format = '%Y%m%d%H%M%S'
            elif args.timezone[0]=='-' or args.timezone[0]=='+':
                tz_format = '%Y%m%d%H%M%S ' + args.timezone
            else:
                tz_format = '%Y%m%d%H%M%S +' + args.timezone
            programme = et.SubElement(top, 'programme', start=starttime.strftime(tz_format), stop=stoptime.strftime(tz_format), channel=str(idtv))
            title = et.SubElement(programme, 'title')
            title.text = unicode_name
            ndx_data = ndx_data[12:]
archive.close()
xmltv=et.ElementTree(element=top)
if args.outputfile !='-':
    xmltv.write(args.outputfile, encoding="utf8", xml_declaration=True)
else:
    print et.tostring(top, encoding='utf8')
