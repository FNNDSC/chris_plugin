from pathlib import Path
from chris_plugin.mapper import _curry_suffix


def test_suffix():
    inputdir = Path('/share/incoming')
    outputdir = Path('/share/outgoing')

    name_mapper = _curry_suffix(inputdir, outputdir, '.fruity')
    input_file = Path('/share/incoming/a/b/c.txt')
    assert name_mapper(input_file) == (outputdir / 'a/b/c.fruity.txt')
