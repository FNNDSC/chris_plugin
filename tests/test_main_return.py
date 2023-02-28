from argparse import Namespace
from pathlib import Path

import pytest

from chris_plugin import chris_plugin


@chris_plugin(singleton=False)
def __returns_none_fs(_options, _path) -> None:
    pass


@chris_plugin(singleton=False)
def __returns_int_fs(_options, _path) -> int:
    return 400


@chris_plugin(singleton=False)
def __returns_none_ds(_options, _p1, _p2) -> None:
    pass


@chris_plugin(singleton=False)
def __returns_int_ds(_options, _p1, _p2) -> int:
    return 500


_options = Namespace()
_path = Path("/tmp")


@pytest.mark.parametrize(
    "result, expected",
    [
        (__returns_none_fs(_options, _path), None),
        (__returns_int_fs(_options, _path), 400),
        (__returns_none_ds(_options, _path, _path), None),
        (__returns_int_ds(_options, _path, _path), 500),
    ],
)
def test_main_return(result, expected):
    assert result == expected
