#!/usr/bin/env python
"""
A short yet complicated *ChRIS* plugin example which uses
`chris_plugin.PathMapper` and `tqdm.contrib.concurrent.thread_map`
to process multiple inputs in parallel while showing a progress bar.
"""

from pathlib import Path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from chris_plugin import chris_plugin, PathMapper
from dataclasses import dataclass
import time
import random
import logging
from tqdm.contrib.concurrent import thread_map
from tqdm.contrib.logging import logging_redirect_tqdm

# configure logging output to show time and thread name
logging.basicConfig(
    format="[%(asctime)s]%(threadName)s:%(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# add command-line arguments
parser = ArgumentParser(
    description="multi-threaded find-and-replace tool",
    formatter_class=ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-i", "--inputPathFilter", default="**/*.txt", help="pattern of files to process"
)
parser.add_argument("-f", "--find", required=True, help="string to find")
parser.add_argument(
    "-r", "--replace", required=False, default="REDACTED", help="word to replace with"
)
parser.add_argument(
    "-t", "--threads", type=int, default=4, help="number of threads to use"
)
parser.add_argument("-s", "--slow", action="store_true", help="throttle performance")


@dataclass
class Replacer:

    find: str
    replace: str
    slow: bool

    def process_file(self, input_file: Path, output_file: Path):
        """
        Iterate over ``input_file`` line-by-line, performing a find-and-replace
        operation, and write the output to ``output_file``.

        If ``self.slow`` is ``True``, sleep for a random amount of time.

        The program's status is printed before processing and upon completion.
        """
        logger.debug('Started "%s"', input_file)
        with input_file.open("r") as input, output_file.open("w") as output:
            for line in input:
                output.write(line.replace(self.find, self.replace))
                if self.slow:
                    time.sleep(random.random())
        logger.debug('Finished "%s"', input_file)


@chris_plugin(
    parser=parser,
    category="Text",
    title="Simple Find and Replace Utility",
    min_cpu_limit="2000m",
)
def main(options, inputdir: Path, outputdir: Path):
    mapper = PathMapper.file_mapper(inputdir, outputdir, glob=options.inputPathFilter)
    r = Replacer(find=options.find, replace=options.replace, slow=options.slow)

    logger.debug(f"Using %d threads", options.threads)
    with logging_redirect_tqdm():
        results = thread_map(
            lambda t: r.process_file(*t),
            mapper,
            max_workers=options.threads,
            total=mapper.count(),
            maxinterval=0.1,
        )

    # if any job failed, an exception will be raised when it's iterated over
    for _ in results:
        pass

    logger.debug("done")


if __name__ == "__main__":
    main()
