import pytest
from datetime import datetime
from jtv2xmltv.parser import parse_titles, parse_schedule


def test_correct_jtv_header():
    data = b'JTV 3.x TV Program Data\x0A\x0A\x0A'
    assert parse_titles(data) == []


def test_incorrect_jtv_header():
    data = b'JTV 3.x TV Program Data\xA0\xA0\xA0'
    with pytest.raises(Exception):
        parse_titles(data)


def test_program_titles():
    data = b'JTV 3.x TV Program Data\x0A\x0A\x0A' \
           b'\x0D\x00First program' \
           b'\x0E\x00Second program'
    assert parse_titles(data) == ['First program', 'Second program']


def test_parse_schedule():
    data = b'\x02\x00' \
           b'\x00\x00\x00\xC0\xF9\x78\xB1\xEE\xD0\x01\x1A\x00' \
           b'\x00\x00\x00\x28\xBE\xDA\xB9\xEE\xD0\x01\x29\x00'
    assert parse_schedule(data) == [datetime(2015, 9, 14, 5, 52), datetime(2015, 9, 14, 6, 52)]
