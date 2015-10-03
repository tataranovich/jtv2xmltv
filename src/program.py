# -*- coding: utf-8 -*-
import struct
import datetime
import sys
import zipfile
import xml.etree.ElementTree as et


#??????big-little ending

reload(sys)
sys.setdefaultencoding('utf8')

filename = "/home/ann/Development/jtv2xmltv-master/examples/TelecomTVepg.zip"
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
        #pdtfile.close()
        ndxfile = archive.open(ndxfile_name, 'r')
        ndx_data=ndxfile.read()
        recnum = ndx_data[0:2]
        ndx_data = ndx_data[2:]
        recordnum = struct.unpack("<H", recnum)
        for i in range(0, recordnum[0]):

            time = ndx_data[2:10]
            #todo вынести преобразование времени в функцию
            filetime = struct.unpack("<Q", time)
            timestamp = filetime[0]/10
            starttime = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp)

            #print recordnum[0]
            if i<> recordnum[0]-1:
                timestop = ndx_data[14:22]
                #print i
                #print len(timestop)
                #todo вынести преобразование времени в функцию
                filetimestop = struct.unpack("<Q", timestop)
                timestampstop = filetimestop[0]/10
                stoptime = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestampstop)
                #print stoptime


            pdt = ndx_data[10:12]
            pdtindex = struct.unpack("<H", pdt)
            pdt_title_offset=pdtindex[0]
            Amt = pdt_data[pdt_title_offset:pdt_title_offset+2]
            Amount = struct.unpack("<H", Amt)
            name = pdt_data[pdt_title_offset+2:pdt_title_offset+2+Amount[0]]
            unicode_name = name.decode('cp1251').encode('UTF-8')
            # TODO добавить возможность указать timezone
            programme = et.SubElement(top, 'programme', start=starttime.strftime('%Y%m%d%H%M%S +0300'), stop=stoptime.strftime('%Y%m%d%H%M%S +0300'), channel=str(idtv))
            title = et.SubElement(programme, 'title')
            title.text = unicode_name
            ndx_data = ndx_data[12:]
archive.close()
#print et.tostring(top, encoding='utf8')
xmltv=et.ElementTree(element=top)
xmltv.write('test.xml', encoding="utf8", xml_declaration=True)