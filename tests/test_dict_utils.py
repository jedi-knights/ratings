import pytest
from datetime import datetime
from ratings.dict_utils import read_str_value, read_int_value, read_datetime_value

@pytest.mark.parametrize("record, key, expected", [
    ({'name': 'John Doe', 'age': '30'}, 'name', 'John Doe'),
    ({'name': 'John Doe', 'age': '30'}, 'age', '30'),
    ({'name': 'John Doe', 'age': '30'}, 'nonexistent', ''),
    ({'key': None}, 'key', '')
])
def test_read_str_value(record, key, expected):
    assert read_str_value(record, key) == expected

@pytest.mark.parametrize("record, key, expected", [
    ({'age': '30', 'score': '100'}, 'age', 30),
    ({'age': '30', 'score': '100'}, 'score', 100),
    ({'age': '30', 'score': '100'}, 'nonexistent', 0),
    ({'key': None}, 'key', 0)
])
def test_read_int_value(record, key, expected):
    assert read_int_value(record, key) == expected

@pytest.mark.parametrize("record, key, expected", [
    ({'date': '2023-10-01T12:00:00'}, 'date', datetime(2023, 10, 1, 12, 0, 0)),
    ({'date': '2023-10-01T12:00:00'}, 'nonexistent', None),
    ({'key': None}, 'key', None)
])
def test_read_datetime_value(record, key, expected):
    assert read_datetime_value(record, key) == expected