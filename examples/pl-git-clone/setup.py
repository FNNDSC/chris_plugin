from setuptools import setup

setup(
    name="git-clone",
    version="1.0.0",
    description="A ChRIS fs plugin for git clone",
    author="FNNDSC",
    author_email="dev@babyMRI.org",
    url="https://github.com/FNNDSC/chris_plugin/tree/master/examples/pl-git-clone",
    py_modules=["git_clone"],
    install_requires=["chris_plugin"],
    license="MIT",
    entry_points={"console_scripts": ["git_clone_wrapper = git_clone:main"]},
)
