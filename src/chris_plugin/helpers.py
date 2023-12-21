"""
General helper functions which might be useful for *ChRIS* plugins.
"""
import sys
from typing import Tuple


def parse_csv_as_dict(s: str):
    """
    Parse a string as a dictionary in the format `key1:value1,key2:value2`.
    Whitespace is ignored. There is no way to escape special characters.
    (This is a workaround for how *ChRIS* does not support repeated
    command-line arguments).

    **On invalid input, an error will be printed, then `sys.exit(1)` is called.**

    Examples:

    - `a:b` -> `{'a': 'b'}`
    - `a:b, c:d` -> `{'a': 'b', 'c': 'd'}`
    """
    if s.strip() == "":
        return {}
    try:
        return {
            p[0].strip(): p[1].strip()
            for p
            in map(__split_on_colon, s.split(','))
        }
    except ValueError as e:
        if any(('not enough values to unpack (expected 2, got 1)' in msg) for msg in e.args):
            print(f'Error parsing "{s}": missing ":"')
            sys.exit(1)
        raise e


def __split_on_colon(s: str) -> Tuple[str, str]:
    a, b = s.split(':', maxsplit=1)
    return a, b
