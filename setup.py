from os import path
from setuptools import setup


with open(path.join(path.dirname(path.abspath(__file__)), "README.md")) as f:
    readme = f.read()


setup(
    name="chris_plugin",
    version="0.1.2",
    packages=["chris_plugin"],
    url="https://github.com/FNNDSC/chris_plugin",
    project_urls={
        "Documentation": "https://fnndsc.github.io/chris_plugin/",
        "Source": "https://github.com/FNNDSC/chris_plugin",
        "Tracker": "https://github.com/FNNDSC/chris_plugin/issues",
    },
    license="MIT",
    author="Jennings Zhang",
    author_email="dev@babyMRI.org",
    description="ChRIS plugin helper",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">= 3.8",
    install_requires=['importlib-metadata; python_version<"3.10"'],
    extras_require={
        'none': [],
        'dev': [
            'pytest~=7.2',
            'pytest-mock~=3.10'
        ]
    },
    entry_points={
        "console_scripts": ["chris_plugin_info = chris_plugin.chris_plugin_info:main"]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
)
