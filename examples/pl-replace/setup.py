from setuptools import setup

setup(
    name             = 'replace',
    version          = '1.0.0',
    description      = 'A ChRIS ds plugin that does a find-and-replace in text files.',
    author           = 'FNNDSC',
    author_email     = 'dev@babyMRI.org',
    url              = 'https://github.com/FNNDSC/chris_plugin/tree/master/examples/pl-replace',
    py_modules       = ['replace'],
    install_requires = ['chris_plugin', 'tqdm'],
    license          = 'MIT',
    python_requires  = '>=3.10.2',
    entry_points     = {
        'console_scripts': [
            'replace = replace:main'
            ]
        }
)
