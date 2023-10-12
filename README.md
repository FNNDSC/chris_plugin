# Python _ChRIS_ Plugin Support

[![codecov](https://codecov.io/gh/FNNDSC/chris_plugin/branch/master/graph/badge.svg?token=TG3CEHU2H4)](https://codecov.io/gh/FNNDSC/chris_plugin)
[![.github/workflows/test.yml](https://github.com/FNNDSC/chris_plugin/actions/workflows/test.yml/badge.svg)](https://github.com/FNNDSC/chris_plugin/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/chris_plugin)](https://pypi.org/project/chris_plugin/)
[![License - MIT](https://img.shields.io/pypi/l/chris_plugin)](https://github.com/FNNDSC/chris_plugin/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

_ChRIS_ is a platform for scientific and medical applications.
https://chrisproject.org/

This repository provides `chris_plugin`, a Python utility library
for writing programs in Python which can run on _ChRIS_.

## Getting Started

Have an existing Python program? See
[HOW TO: Convert an existing Python app](https://github.com/FNNDSC/chris_plugin/wiki/HOW-TO:-Convert-an-existing-Python-app)
into a _ChRIS_ _ds_ plugin.

If you're creating a **new** program,
you can start from this template:
https://github.com/FNNDSC/python-chrisapp-template

Examples can be found in [./examples](./examples).

## Usage

After developing a plugin, use the command `chris_plugin_info`
to produce a JSON description of your *ChRIS* plugin.

```shell
chris_plugin_info --dock-image {registry}/{repo}/{name}:{version} [module_name]
```

If `module_name` is not given, then `chris_plugin_info`
will automatically discover your *ChRIS* plugin.

## Development Goals

`chris_plugin` strives to have zero-dependencies and compatible with Python 3.8 through 3.12.
