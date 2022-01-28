# Python _ChRIS_ Plugin Support

[![.github/workflows/test.yml](https://github.com/FNNDSC/chris_plugin/actions/workflows/test.yml/badge.svg)](https://github.com/FNNDSC/chris_plugin/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/chris_plugin)](https://pypi.org/project/chris_plugin/)
[![License - MIT](https://img.shields.io/pypi/l/chris_plugin)](https://github.com/FNNDSC/chris_plugin/blob/master/LICENSE)

_ChRIS_ is a platform for scientific and medical applications.
https://chrisproject.org/

This repository provides `chris_plugin`, a Python package for writing
programs in Python which can run on _ChRIS_.

## Getting Started

Have an existing Python program? See
[HOW TO: Convert an existing Python app](https://github.com/FNNDSC/chris_plugin/wiki/HOW-TO:-Convert-an-existing-Python-app)
into a _ChRIS_ _ds_ plugin.

If you're creating a **new** program,
you can start from a template.

Github template repository: https://github.com/FNNDSC/python-chrisapp-template

A more comprehensive starting point can be created using
[cookiecutter](https://cookiecutter.readthedocs.io):

```shell
cookiecutter https://github.com/FNNDSC/cookiecutter-chrisapp
```

## Usage

After developing a plugin, use the command `chris_plugin_info`
to produce a JSON description of your *ChRIS* plugin.

```shell
chris_plugin_info [module_name]
```

If `module_name` is not given, then `chris_plugin_info`
will automatically discover your *ChRIS* plugin.
