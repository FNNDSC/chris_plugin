import argparse
import importlib
import shutil
import sys
from pathlib import Path
from typing import Iterable, Optional, Tuple, List, Dict
import json
from chris_plugin._registration import get_registered
from chris_plugin.parameters import serialize
import chris_plugin.links as links

from importlib.metadata import Distribution, distribution

try:
    # new in Python 3.10
    from importlib.metadata import packages_distributions
except ImportError:
    from importlib_metadata import packages_distributions

import logging

logging.basicConfig()


parser = argparse.ArgumentParser(description="Get ChRIS plugin description")
parser.add_argument(
    "distribution",
    nargs="?",
    help="Distribution name of Python ChRIS plugin, i.e. the "
    "name given to your project in setup.py. "
    "If unspecified, tries to guess the module name by "
    "querying for which installed pip package depends on "
    f'"{__package__}"',
)


class GuessException(Exception):
    """
    `chris_module_info` was unable to automatically detect any installed *ChRIS* plugins.
    """

    pass


def get_all_distributions() -> Iterable[Distribution]:
    return map(distribution, get_all_distribution_names())


def get_all_distribution_names() -> Iterable[str]:
    return (
        dist
        for dists_per_package in packages_distributions().values()
        for dist in dists_per_package
    )


def underscore(s: str) -> str:
    """
    Python packaging is very inconsistent. Even though this package's
    name is "chris_plugin", its _distribution's_ name might appear as

    "chris-plugin" in some situations but not all.
    e.g. when the plugin is installed via:

        `pip install -e `                           => d.requires = ['chris_plugin']
        `pip install --use-feature=in-tree-build .` => d.requires = ['chris_plugin']

    :param s: string
    :return: given string with '-' replaced by '_'
    """
    return s.replace("-", "_")


def strip_version(r: str) -> str:
    """
    :param r: required package name and required version matcher
    :return: just the package name
    """
    for symbol in [" ", "~", "<", ">", "="]:
        i = r.find(symbol)
        if i != -1:
            return r[:i].rstrip()
    return r


def get_dependents() -> Iterable[Distribution]:
    return filter(is_dependent, get_all_distributions())


def dedupe(deps: Iterable[Distribution]) -> Dict[str, Distribution]:
    return {d.name: d for d in deps}


def is_dependent(d: Distribution) -> bool:
    if d.requires is None:
        return False
    return "chris_plugin" in map(strip_version, map(underscore, d.requires))


def guess_plugin_distribution() -> Distribution:
    dependents = dedupe(get_dependents())
    if len(dependents) < 1:
        print(
            'Could not find ChRIS plugin. Make sure you have "pip installed" '
            "your ChRIS plugin as a python package.",
            file=sys.stderr,
        )
        sys.exit(1)
    if len(dependents) > 1:
        print(
            "Found multiple ChRIS plugin distributions, "
            "please specify one: " + str(list(dependents.keys())),
            file=sys.stderr,
        )
        sys.exit(1)
    (single_dependent,) = dependents.values()
    return single_dependent


def get_distribution(name: str) -> Distribution:
    dependents = dedupe(get_dependents())
    if name not in dependents:
        print(
            f"Could not find dependent Python distribution by name: {name}."
            f"Available options: {list(dependents.keys())}",
            file=sys.stderr,
        )
    return dependents[name]


def entrypoint_modules(_d: Distribution) -> List[str]:
    return [
        ep.value[: ep.value.index(":")]
        for ep in _d.entry_points
        if ep.group == "console_scripts"
    ]


def entrypoint_of(d: Distribution) -> str:
    eps = [ep for ep in d.entry_points if ep.group == "console_scripts"]
    if not eps:
        print(
            f'"{d.name}" does not have any console_scripts defined in its setup.py.\n'
            f"For help, see {links.setup_py_help}",
            file=sys.stderr,
        )
        sys.exit(1)
    if len(eps) > 1:
        # multiple console_scripts found, but maybe they're just the same thing
        if len(frozenset(eps)) > 1:
            print(
                f'Multiple console_scripts found for "{d.name}": {str(eps)}',
                file=sys.stderr,
            )
    return eps[0].name


def get_or_guess(name: Optional[str]) -> Tuple[List[str], Distribution]:
    dist = get_distribution(name) if name else guess_plugin_distribution()
    mods = entrypoint_modules(dist)
    if not mods:
        print(
            f"No entrypoint modules found for {dist.name}. "
            "In your ChRIS plugin's setup.py, please specify "
            "entry_points={'console_scripts': [...]}",
            file=sys.stderr,
        )
        sys.exit(1)
    return mods, dist


def main():
    args = parser.parse_args()
    mods, dist = get_or_guess(args.distribution)
    for module_name in mods:
        importlib.import_module(module_name)
    details = get_registered()
    setup = dist.metadata
    command = Path(shutil.which(entrypoint_of(dist)))
    info = {
        "type": details.type,
        "parameters": serialize(details.parser),
        "icon": details.icon,
        "authors": f'{setup["Author"]} <{setup["Author-email"]}>',
        "title": details.title if details.title else setup["Name"],
        "category": details.category,
        "description": setup["Summary"],
        "documentation": setup["Home-page"],
        "license": setup["License"],
        "version": setup["Version"],
        # ChRIS_ultron_backEnd version 2.8.1 requires these three to be defined
        # https://github.com/FNNDSC/ChRIS_ultron_backEnd/blob/fd38ae519dd1baf59c27677eb5a8ba774dc5f198/chris_backend/plugins/models.py#L174-L176
        "selfpath": str(command.parent),
        "selfexec": str(command.name),
        "execshell": sys.executable,
        "min_number_of_workers": details.min_number_of_workers,
        "max_number_of_workers": details.max_number_of_workers,
        "min_memory_limit": details.min_memory_limit,
        "max_memory_limit": details.max_memory_limit,
        "min_cpu_limit": details.min_cpu_limit,
        "max_cpu_limit": details.max_cpu_limit,
        "min_gpu_limit": details.min_gpu_limit,
        "max_gpu_limit": details.max_gpu_limit,
    }
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
