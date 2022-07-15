"""
# Python *ChRIS* Plugin Support

[`chris_plugin`](https://pypi.org/project/chris-plugin/)
is a library for writing
[*ChRIS*](https://chrisproject.org/) plugins.

## Getting Started

Take a look at the
[README](https://github.com/FNNDSC/chris_plugin#readme)
and [examples](https://github.com/FNNDSC/chris_plugin/tree/master/examples).

A walk-through can be found on our
[wiki](https://github.com/FNNDSC/chris_plugin/wiki/HOW-TO:-Convert-an-existing-Python-app).

## Core API

`chris_plugin` is a decorator which transforms an ordinary
python function into a *ChRIS* plugin.

```python
from chris_plugin import chris_plugin
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--name', required=True)

@chris_plugin(parser=parser, title='Example')
def main(options, inputdir, outputdir):
    print(f'hello, {parser.name}')
```

## Helper Functions

This library also provides helper functions for common patterns,
such as `chris_plugin.PathMapper`.

```python
import shutil
from chris_plugin import chris_plugin, PathMapper

@chris_plugin
def main(_, input_dir, output_dir):
    for input_file, output_file in PathMapper.file_mapper(input_dir, output_dir):
        print(f'Copying {input_file} to {output_file}')
        shutil.copy(input_file, output_file)
```

"""

from chris_plugin.chris_plugin import chris_plugin
from chris_plugin.mapper import PathMapper
import chris_plugin.types as types

__docformat__ = "numpy"

__all__ = ["chris_plugin", "PathMapper", "types"]
