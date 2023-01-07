import pytest

from argparse import Namespace
from pathlib import Path
from chris_plugin.main_function import is_plugin_main, is_ds, is_fs
import tests.examples.main_functions as examples


def test_no_args():
    def takes_no_args():
        pass

    em = (
        "A ChRIS plugin's main function must accept "
        "its options as its first argument"
    )
    with pytest.raises(ValueError, match=em):
        is_plugin_main(takes_no_args)


def test_too_few():
    def too_few(a):
        pass

    em = (
        "A ChRIS plugin's main function must accept "
        "an argument for its output directory"
    )
    with pytest.raises(ValueError, match=em):
        is_plugin_main(too_few)


def test_too_many():
    def too_many(a, b, c, d):
        pass

    em = "A ChRIS plugin's main function cannot " "take more than 3 arguments"
    with pytest.raises(ValueError, match=em):
        is_plugin_main(too_many)


def test_bad_options_type():
    def bad_options_type(a: int, b: Path):
        pass

    em = (
        "A ChRIS plugin's main function must accept "
        "its options as its first argument"
    )
    with pytest.raises(ValueError, match=em):
        is_plugin_main(bad_options_type)


def test_bad_path_type():
    def bad_path_type1(a: Namespace, b: int):
        pass

    def bad_path_type2(a: Namespace, b: Path, c: str):
        pass

    em = "A ChRIS plugin's data directory arguments " "must have type pathlib.Path"
    for example in [bad_path_type1, bad_path_type2]:
        with pytest.raises(ValueError, match=em):
            is_plugin_main(example)


def test_is_good_main():
    assert is_plugin_main(examples.ok_ds1)
    assert is_plugin_main(examples.ok_ds2)
    assert is_plugin_main(examples.ok_fs1)
    assert is_plugin_main(examples.ok_fs2)


def test_is_fs():
    assert is_fs(examples.ok_fs1)
    assert is_fs(examples.ok_fs2)
    assert not is_fs(examples.ok_ds1)
    assert not is_fs(examples.ok_ds2)


def test_is_ds():
    assert is_ds(examples.ok_ds1)
    assert is_ds(examples.ok_ds2)
    assert not is_ds(examples.ok_fs1)
    assert not is_ds(examples.ok_fs2)
