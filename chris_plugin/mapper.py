from pathlib import Path
import functools
from typing import Callable, TypeVar, Any, Protocol

_T = TypeVar('_T')


class FunctionCaller(Protocol):
    """
    A type which describes functions which call a given function.
    """
    def __call__(self, __fn: Callable[..., _T], *args: Any, **kwargs: Any) -> Any:
        ...


def call(__fn: Callable[..., _T], *args: Any, **kwargs: Any) -> _T:
    """
    Literally just call it.
    """
    return __fn(*args, **kwargs)


def vectorize(
        func: Callable[[Path], Path] = None, /, *,
        name_mapper: str | Callable[[Path], Path] = None,
        parents: bool = True,
        glob: str = '**/*',
        executor: FunctionCaller = call
):
    """
    Creates a decorator which changes a function that operates on
    single files to one that processes every file in a directory.

    :param func: if used directly without parens, first argument should be the
                 function to wrap
    :param name_mapper: either a string which is appended to the file name
                        before the file extension of the input file to get
                        the output file name, or a function which, given
                        the input file name, produces the output file name
    :param parents: if True, create parent directories as needed
    :param glob: file name pattern
    :param executor: used to make calls to the decorated function. Concurrency
                     can be achieved by using a :meth:`concurrent.futures.Executor.submit`
    """
    def wrap(fn: Callable[[Path], Path]):
        @functools.wraps(fn)
        def wrapper(inputdir: Path, outputdir: Path):
            get_output_name = name_mapper
            if get_output_name is None:
                get_output_name = ''
            if isinstance(get_output_name, str):
                get_output_name = curry_suffix(inputdir, outputdir, get_output_name)

            for input_file in inputdir.glob(glob):
                if not input_file.is_file():
                    continue
                output_file = get_output_name(input_file)
                if parents:
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                executor(fn, input_file, output_file)
        return wrapper

    # See if we're being called as @vectorize or @vectorize().
    if func is None:
        # We're called with parens.
        return wrap

    # We're called as @vectorize without parens.
    return wrap(func)


def curry_suffix(inputdir: Path, outputdir: Path, suffix: str) -> Callable[[Path], Path]:
    def append_suffix(input_file: Path) -> Path:
        rel = input_file.relative_to(inputdir)
        return (outputdir / rel).with_stem(input_file.stem + suffix)
    return append_suffix
