from __future__ import print_function
import argparse
import sys
from jtv2xmltv.convert import convert_jtv_to_xmltv


def main():
    if int(sys.version[0]) == 2:
        # Undefined variable 'reload'
        # pylint: disable=E0602
        reload(sys)
        # Module 'sys' has no 'setdefaultencoding' member
        # pylint: disable=E1101
        sys.setdefaultencoding('utf8')
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
    xmltv_content = convert_jtv_to_xmltv(jtv_filename, epg_timezone=tz_format)
    if xmltv_filename is None or xmltv_filename == "-":
        print(xmltv_content)
    else:
        xmltv = open(xmltv_filename, 'w')
        xmltv.write(xmltv_content)
        xmltv.close()
