import os
from jtv2xmltv.convert import convert_jtv_to_xmltv


def test_jtv_to_xmltv_convert():
    expected = '<?xml version=\'1.0\' encoding=\'utf8\'?>\n' \
               '<tv><channel id="1"><display-name>Sample channel</display-name></channel>' \
               '<programme channel="1" start="20150914055200" stop="20150914065200">' \
               '<title>First program</title></programme>' \
               '<programme channel="1" start="20150914065200"><title>Second program</title></programme></tv>'

    tests_dir = os.path.dirname(os.path.realpath(__file__))
    result = convert_jtv_to_xmltv(os.path.join(tests_dir, 'data/sample.zip'))
    assert expected == result
