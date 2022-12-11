import pytest
from datetime import datetime
from jtv2xmltv.parser import is_valid_jtv, get_program_title, parse_schedule


def test_correct_jtv_header():
    data = b'JTV 3.x TV Program Data\x0A\x0A\x0A'
    assert is_valid_jtv(data) is True


def test_alternative_jtv_header():
    data = b'JTV 3.x TV Program Data\xA0\xA0\xA0'
    assert is_valid_jtv(data) is True


def test_incorrect_jtv_header():
    data = b'JTV 3.x TV Program Data\xFF\xFF\xFF'
    assert is_valid_jtv(data) is False


def test_program_titles():
    data = b'JTV 3.x TV Program Data\x0A\x0A\x0A' \
           b'\x0D\x00First program' \
           b'\x0E\x00Second program'
    assert get_program_title(data, 26) == 'First program'


def test_parse_schedule():
    ndx_data = b'\x02\x00' \
           b'\x00\x00\x00\xC0\xF9\x78\xB1\xEE\xD0\x01\x1A\x00' \
           b'\x00\x00\x00\x28\xBE\xDA\xB9\xEE\xD0\x01\x29\x00'
    pdt_data = b'JTV 3.x TV Program Data\x0A\x0A\x0A' \
        b'\x0D\x00First program' \
        b'\x0E\x00Second program'
    expected_result = [
        {'time': datetime(2015, 9, 14, 5, 52), 'title': 'First program'},
        {'time': datetime(2015, 9, 14, 6, 52), 'title': 'Second program'}
    ]
    assert parse_schedule(ndx_data, pdt_data) == expected_result
