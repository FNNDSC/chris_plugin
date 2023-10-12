from setuptools import setup

setup(
    name="simple_copy",
    version="1.0.0",
    description="A ChRIS ds plugin that copies data",
    author="FNNDSC",
    author_email="dev@babyMRI.org",
    url="https://github.com/FNNDSC/chris_plugin/tree/master/examples/pl-copy",
    py_modules=["simple_copy"],
    install_requires=["chris_plugin"],
    license="MIT",
    python_requires=">=3.10.2",
    entry_points={"console_scripts": ["simple_copy = simple_copy:main"]},
)
