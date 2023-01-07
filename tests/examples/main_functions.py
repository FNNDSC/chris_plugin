from argparse import Namespace
from pathlib import Path


def ok_fs1(a: Namespace, b: Path) -> None:
    pass


def ok_fs2(a, b):
    pass


def ok_ds1(a: Namespace, b: Path, c: Path):
    pass


def ok_ds2(a, b, c) -> None:
    pass
