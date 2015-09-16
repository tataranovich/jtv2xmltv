#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import zipfile

reload(sys)
sys.setdefaultencoding('utf8')

filename = sys.argv[1]

archive = zipfile.ZipFile(filename, 'r')

for filename in archive.namelist():
    if filename.endswith('.pdt'):
        try:
            unicode_name = filename.decode('UTF-8').encode('UTF-8')
        except:
            unicode_name = filename.decode('cp866').encode('UTF-8')
        channel_name = unicode_name[0:-4]
        print channel_name