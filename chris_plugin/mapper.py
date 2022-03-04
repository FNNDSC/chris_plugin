import sys
from pathlib import Path
from typing import Callable, ClassVar, Iterable, Iterator, Tuple, Optional
from dataclasses import dataclass, InitVar


NameMapper = Callable[[Path, Path], Path]


def _verbatim(input_file: Path, output_dir: Path) -> Path:
    return output_dir / input_file


def _curry_suffix(suffix: str) -> NameMapper:
    def append_suffix(input_file: Path, output_dir: Path) -> Path:
        return (output_dir / input_file).with_suffix(suffix)
    return append_suffix


def _exit(mapper: 'PathMapper') -> None:
    print(f'warning: no input found for "{mapper.input_dir / mapper.glob}"', file=sys.stderr)
    sys.exit(1)


@dataclass(frozen=True)
class PathMapper(Iterable[Tuple[Path, Path]]):
    """
    An iterator which discovers input files in a directory and maps
    them to output path names.

    For example, an input file `/share/incoming/a/b/c.txt` will be
    mapped to `/share/outgoing/a/b/c.txt`.

    A common use case would be *ChRIS* *ds* plugins which operate
    on individual input files.

    Examples
    --------

    Copy all files from `input_dir` to `output_dir`:

    ```python
    for input_file, output_file in PathMapper(input_dir, output_dir):
        shutil.copy(input_file, output_file)
    ```


    Avoid clobbering (overwriting existing files):

    ```python
    for input_file, output_file in PathMapper(input_dir, output_dir):
        if output_file.exists():
            print(f'error, file exists: {output_file}', sys.stderr)
            sys.exit(1)
        shutil.copy(input_file, output_file)
    ```

    Call the function `segmentation` on only NIFTI files, and rename output
    file names to end with `.seg.nii`:

    ```python
    mapper = PathMapper(input_dir, output_dir, glob='**/*.nii', suffix='.seg.nii')
    for input_file, output_file in mapper:
        segmentation(input_file, output_file)
    ```

    Use [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor)
    to parallelize subprocesses:


    ```python
    import subprocess as sp
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=4) as pool:
        for input_file, output_path in PathMapper(input_dir, output_dir):
            pool.submit(sp.run, ['external_command', input_file, output_path])
    ```

    The program works similarly to the usage of GNU
    [parallel](https://www.gnu.org/software/parallel/).

    Hint: `len(os.sched_getaffinity(0))` gets the number of CPUs available
    to a containerized process (which can be limited by, for instance,
    `docker run --cpuset-cpus 0-3`)

    Add a progress bar with [tqdm](https://github.com/tqdm/tqdm):

    ```python
    from tqdm import tqdm

    mapper = PathMapper(input_dir, output_dir)
    with tqdm(total=mapper.count()) as bar:
        for input_file, output_path in PathMapper(input_dir, output_dir):
            do_something(input_file, output_path)
            bar.update()
    ```
    """

    input_dir: Path
    """Directory containing input files"""
    output_dir: Path
    """Directory for output files to be written to"""

    suffix: InitVar[str] = None
    """
    If specified, replace output path file extension with given value.
    """
    name_mapper: InitVar[NameMapper] = _verbatim
    """
    Specify a custom function which produces an output file name given the
    input path relative to `input_dir`, and `output_dir`.
    
    Only one of [`suffix`, `name_mapper`] can be given.
    """
    _name_mapper: ClassVar[NameMapper] = None

    glob: str = '**/*'
    """
    File name pattern matching input files in `input_dir`.
    """
    only_files: bool = True
    """
    If `True`, yield only files.
    """
    parents: bool = True
    """
    If `True`, create parent directories of output paths as needed.
    """
    empty_action: Optional[Callable[['PathMapper'], None]] = _exit
    """
    Function to call if input is empty. This function is given self.
    The default is to print a warning, then call `sys.exit(1)`. 
    """

    def __post_init__(self, suffix: str, name_mapper: Callable[[Path], Path]):
        if suffix is not None:
            if name_mapper is not _verbatim:
                raise ValueError('Cannot specify both suffix and non-default name_mapper')
            return object.__setattr__(self, '_name_mapper', _curry_suffix(suffix))
        if name_mapper is None:
            raise ValueError('name_mapper cannot be None')
        object.__setattr__(self, '_name_mapper', name_mapper)

    def __should_include(self, input_file: Path) -> bool:
        if self.only_files:
            return input_file.is_file()
        return True

    def iter_input(self) -> Iterator[Path]:
        """
        :return: an iterator over input files
        """
        return (
            input_file for input_file in self.input_dir.glob(self.glob)
            if self.__should_include(input_file)
        )

    def count(self) -> int:
        """
        :return: number of input files
        """
        c = 0
        for _ in self.iter_input():
            c += 1
        return c

    def __iter__(self) -> Iterator[Tuple[Path, Path]]:
        is_empty = True
        for input_file in self.iter_input():
            rel = input_file.relative_to(self.input_dir)
            output_file = self._name_mapper(rel, self.output_dir)
            if self.parents:
                output_file.parent.mkdir(parents=True, exist_ok=True)
            yield input_file, output_file
            is_empty = False
        if is_empty and self.empty_action is not None:
            self.empty_action(self)
