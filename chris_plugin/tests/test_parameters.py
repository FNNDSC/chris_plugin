import pytest
from argparse import ArgumentParser
from chris_plugin.types import Special, ParameterSpec
from chris_plugin.constants import Placeholders
from chris_plugin._parameters import serialize_store_action, get_param_type


@pytest.fixture
def parser() -> ArgumentParser:
    return ArgumentParser()


def test_required_int(parser: ArgumentParser):
    action = parser.add_argument('-n', '--number', type=int, required=True,
                                 default=1, help='an integer value')
    expected = ParameterSpec(
        name='number',
        type='int',
        optional=False,
        flag='--number',
        short_flag='-n',
        action='store',
        help='an integer value',
        default=1,
        ui_exposed=True
    )
    assert serialize_store_action(action) == expected


def test_optional_int(parser: ArgumentParser):
    action = parser.add_argument('-a', '--aa', type=int, required=False,
                                 help='aaa')
    expected = ParameterSpec(
        name='aa',
        type='int',
        optional=True,
        flag='--aa',
        short_flag='-a',
        action='store',
        help='aaa',
        default=Placeholders.INT,
        ui_exposed=True
    )
    assert serialize_store_action(action) == expected


def test_without_short(parser: ArgumentParser):
    action = parser.add_argument('--aa', type=str, help='aaa')
    expected = ParameterSpec(
        name='aa',
        type='str',
        optional=True,
        flag='--aa',
        short_flag='--aa',
        action='store',
        help='aaa',
        default=Placeholders.STR,
        ui_exposed=True
    )
    assert serialize_store_action(action) == expected


def test_everything_default(parser: ArgumentParser):
    action = parser.add_argument('--aa')
    # TODO assert warnings are printed
    expected = ParameterSpec(
        name='aa',
        type='str',
        optional=True,
        flag='--aa',
        short_flag='--aa',
        action='store',
        help='',
        default=Placeholders.STR,
        ui_exposed=True
    )
    assert serialize_store_action(action) == expected


def test_get_param_type(parser: ArgumentParser):
    p = parser.add_argument('-q', type=Special.path, required=True)
    assert get_param_type(p) == 'path'
    p = parser.add_argument('-w', type=Special.unextpath, required=True)
    assert get_param_type(p) == 'unextpath'
    p = parser.add_argument('-e')
    assert get_param_type(p) == 'str'
    p = parser.add_argument('-r', default=1.0)
    assert get_param_type(p) == 'float'
    p = parser.add_argument('-t', type=int)
    assert get_param_type(p) == 'int'


def test_special_serializer(parser: ArgumentParser):
    pass  # TODO


def test_special_required():
    pass  # TODO


def test_subparsers_not_allowed():
    pass  # TODO


def test_groups():
    pass  # TODO


def test_mutually_exclusive_groups():
    pass  # TODO

