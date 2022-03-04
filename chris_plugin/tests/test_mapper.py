import sys
from pathlib import Path
from typing import Tuple, List

import pytest
from pytest_mock import MockerFixture

from chris_plugin.mapper import _curry_suffix, PathMapper


def test_suffix():
    name_mapper = _curry_suffix('.fruity')
    input_file = Path('a/b/c.txt')
    output_dir = Path('/share/outgoing')
    assert name_mapper(input_file, output_dir) == (output_dir / 'a/b/c.fruity')


@pytest.fixture
def dirs(tmp_path: Path) -> Tuple[Path, Path]:
    return tmp_path / 'incoming', tmp_path / 'outgoing'


@pytest.fixture
def files_to_create(dirs: Tuple[Path, Path]) -> List[str]:
    input_dir, output_dir = dirs
    files = [
        'a/b/crane.txt',
        'coco.txt',
        'beryl.rb',
        'johannesburg'
    ]
    for f in files:
        fp = input_dir / f
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.touch(exist_ok=True)
    return files


def test_basic(dirs: Tuple[Path, Path], files_to_create: List[str]):
    inputdir, outputdir = dirs
    input_files = [inputdir / f for f in files_to_create]

    visited: set[Path] = set()
    output_files: set[Path] = set()

    for i, o in PathMapper(inputdir, outputdir):
        assert i not in visited, f'{i} visited twice'
        assert i in input_files, f'{i} is not a valid input file'
        assert o.parent.exists()
        assert not o.exists()
        visited.add(i)
        output_files.add(o)

    assert set(output_files) == set(outputdir / f for f in files_to_create)


def test_no_parent(dirs: Tuple[Path, Path], files_to_create: List[str]):
    inputdir, outputdir = dirs
    for i, o in PathMapper(inputdir, outputdir, parents=False):
        if i.name == 'crane.txt':
            assert not o.parent.exists()


def test_empty_action(mocker: MockerFixture, tmp_path: Path):
    input_dir = tmp_path
    output_dir = tmp_path / 'output'
    mock_print = mocker.patch('builtins.print')
    with pytest.raises(SystemExit):
        for i, o in PathMapper(input_dir, output_dir, glob='**/*.something'):
            pytest.fail('Test is messed up, input should be empty')
    mock_print.assert_called_once_with(
        f'warning: no input found for "{input_dir / "**/*.something"}"', file=sys.stderr
    )
