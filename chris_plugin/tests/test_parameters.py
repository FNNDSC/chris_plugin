import pytest
from argparse import ArgumentParser
from chris_plugin.types import Special, ParameterSpec
from chris_plugin.constants import Placeholders
from chris_plugin.parameters import serialize_store_action, get_param_type, serialize, should_include


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


def test_serialize_choices(parser: ArgumentParser):
    p = parser.add_argument('-a', '--apple', choices=('red', 'green'),
                            help='Crispy fruit')
    expected = ParameterSpec(
        name='apple',
        type='str',
        optional=True,
        flag='--apple',
        short_flag='-a',
        action='store',
        help='Crispy fruit [choices: red, green]',
        default=Placeholders.STR,
        ui_exposed=True
    )
    assert serialize_store_action(p) == expected


def test_serialize_choices_num(parser: ArgumentParser):
    p = parser.add_argument('-n', '--num', choices=range(1, 9, 3),
                            default=4, help='Pick a lucky one')
    expected = ParameterSpec(
        name='num',
        type='int',
        optional=True,
        flag='--num',
        short_flag='-n',
        action='store',
        help='Pick a lucky one [choices: 1, 4, 7]',
        default=4,
        ui_exposed=True
    )
    assert serialize_store_action(p) == expected


def test_version_option_is_allowed(parser: ArgumentParser):
    p = parser.add_argument('-V', '--version', action='version',
                            version='$(prog)s 1.2.3')
    assert not should_include(p)
    assert serialize(parser) == []


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

