"""
# !!! WIP !!!

Helper functions to get the resource limits of the container
this process is running in.
"""

import os
from pathlib import Path
from typing import Callable

__CGROUP_MEMORY_LIMIT_FILE = Path('/sys/fs/cgroup/memory/memory.limit_in_bytes')


def _linux_only(f: Callable) -> Callable:
    """
    A decorator which denotes the function is only supported on Linux.
    """
    ...


def get_cpu_count() -> int:
    """
    Number of CPUs visible to the container this process is running in.
    """
    return len(os.sched_getaffinity(0))


def get_memory_limit() -> int:
    """

    Returns
    -------

    Memory limit in bytes.
    """

    try:
        t = __CGROUP_MEMORY_LIMIT_FILE.read_text()
        return int(t)
    except FileNotFoundError:
        ...
