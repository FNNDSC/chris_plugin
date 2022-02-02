import argparse
import importlib
import shutil
import sys
from importlib.metadata import Distribution, distribution, packages_distributions
from typing import Iterable, Optional
import json

from chris_plugin._registration import get_registered
from chris_plugin.parameters import serialize
import chris_plugin.links as links

import logging
logging.basicConfig()


parser = argparse.ArgumentParser(description='Get ChRIS plugin description')
parser.add_argument('module_name', nargs='?',
                    help='module name of Python ChRIS plugin. '
                         'If unspecified, tries to guess the module name by '
                         'querying for which installed pip package depends on '
                         f'"{__package__}"')


class GuessException(Exception):
    """
    `chris_module_info` was unable to automatically detect any installed *ChRIS* plugins.
    """
    pass


def get_all_distributions() -> Iterable[Distribution]:
    return map(distribution, get_all_distribution_names())


def get_all_distribution_names() -> Iterable[str]:
    return (
        dist for dists_per_package in packages_distributions().values()
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
    return s.replace('-', '_')


def get_dependents() -> Iterable[Distribution]:
    return filter(is_dependent, get_all_distributions())


def is_dependent(d: Distribution) -> bool:
    if d.requires is None:
        return False
    return 'chris_plugin' in map(underscore, d.requires)


def guess_plugin_distribution() -> Distribution:
    dependents = set(get_dependents())
    if len(dependents) < 1:
        print(
            'Could not find ChRIS plugin. Make sure you have "pip installed" '
            'your ChRIS plugin as a python package.',
            file=sys.stderr
        )
        sys.exit(1)
    if len(dependents) > 1:
        print(
            'Found multiple ChRIS plugin distributions, '
            'please specify one: ' +
            str([underscore(d.name) for d in dependents]),
            file=sys.stderr
        )
        sys.exit(1)
    dist, = dependents
    return dist


def get_distribution_of(module_name: str) -> Distribution:
    dot = module_name.find('.')
    if dot != -1:
        module_name = module_name[:dot + 1]
    # idk why it's a list, i don't want to deal with it
    dist_names = packages_distributions().get(module_name)
    if not dist_names:
        print(f'No distribution found for module: {module_name}', file=sys.stderr)
        if '-' in module_name:
            fixed_name = module_name.replace('-', '_')
            print(f'Hint: try "{fixed_name}"', file=sys.stderr)
        sys.exit(1)
    return distribution(dist_names[0])


def entrypoint_modules(_d: Distribution) -> list[str]:
    return [
        ep.value[:ep.value.index(':')]
        for ep in _d.entry_points
        if ep.group == 'console_scripts'
    ]


def entrypoint_of(d: Distribution) -> str:
    eps = [ep for ep in d.entry_points if ep.group == 'console_scripts']
    if not eps:
        print(f'"{d.name}" does not have any console_scripts defined in its setup.py.\n'
              f'For help, see {links.setup_py_help}', file=sys.stderr)
        sys.exit(1)
    if len(eps) > 1:
        # multiple console_scripts found, but maybe they're just the same thing
        if len(frozenset(eps)) > 1:
            print(f'Multiple console_scripts found for "{d.name}": {str(eps)}', file=sys.stderr)
    return eps[0].name


def get_or_guess(module_name: Optional[str]) -> tuple[list[str], Distribution]:
    if module_name:
        return [module_name], get_distribution_of(module_name)
    dist = guess_plugin_distribution()
    mods = entrypoint_modules(dist)
    if not mods:
        print(f'No entrypoint modules found for {dist.name}. '
              "In your ChRIS plugin's setup.py, please specify "
              "entry_points={'console_scripts': [...]}",
              file=sys.stderr)
        sys.exit(1)
    return mods, dist


def main():
    args = parser.parse_args()
    mods, dist = get_or_guess(args.module_name)
    for module_name in mods:
        importlib.import_module(module_name)
    details = get_registered()
    setup = dist.metadata
    command = entrypoint_of(dist)
    info = {
        'type': details.type,
        'parameters': serialize(details.parser),
        'icon': details.icon,
        'authors': f'{setup["Author"]} <{setup["Author-email"]}>',
        'title': details.title if details.title else setup['Name'],
        'category': details.category,
        'description': setup['Summary'],
        'documentation': setup['Home-page'],
        'license': setup['License'],
        'version': setup['Version'],

        # ChRIS_ultron_backEnd version 2.8.1 requires these three to be defined
        # https://github.com/FNNDSC/ChRIS_ultron_backEnd/blob/fd38ae519dd1baf59c27677eb5a8ba774dc5f198/chris_backend/plugins/models.py#L174-L176
        'selfpath': shutil.which(command),
        'selfexec': command,
        'execshell': sys.executable,

        'min_number_of_workers': details.min_number_of_workers,
        'max_number_of_workers': details.max_number_of_workers,
        'min_memory_limit': details.min_memory_limit,
        'max_memory_limit': details.max_memory_limit,
        'min_cpu_limit': details.min_cpu_limit,
        'max_cpu_limit': details.max_cpu_limit,
        'min_gpu_limit': details.min_gpu_limit,
        'max_gpu_limit': details.max_gpu_limit
    }
    print(json.dumps(info, indent=2))


if __name__ == '__main__':
    main()