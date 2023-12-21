import pytest

from chris_plugin.helpers import parse_csv_as_dict


@pytest.mark.parametrize('input, expected', [
    ["", {}],
    ["a:b", {'a': 'b'}],
    ["a:b,c:d", {'a': 'b', 'c': 'd'}],
    ["a:b, c:d", {'a': 'b', 'c': 'd'}],
    ["a:b, c:d, e: f", {'a': 'b', 'c': 'd', 'e': 'f'}],
])
def test_parse_csv_as_dict(input: str, expected: dict):
    assert parse_csv_as_dict(input) == expected


@pytest.mark.parametrize('input', [
    "a",
    "a b"
])
def test_parse_csv_as_dict_errors(input: str):
    with pytest.raises(SystemExit):
        parse_csv_as_dict(input)
