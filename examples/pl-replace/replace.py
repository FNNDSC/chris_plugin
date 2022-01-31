#!/usr/bin/env python
"""
A short yet complicated *ChRIS* plugin example which uses
`chris_plugin.PathMapper`, `concurrent.futures.ThreadPoolExecutor`,
and `tqdm.tqdm`.
"""

from pathlib import Path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from chris_plugin import chris_plugin, PathMapper
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import time
import random
import logging
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

logging.basicConfig(format='[%(asctime)s]%(threadName)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

parser = ArgumentParser(description='multi-threaded find-and-replace tool',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--inputPathFilter',
                    default='**/*.txt',
                    help='pattern of files to process')
parser.add_argument('-f', '--find', required=True, help='string to find')
parser.add_argument('-r', '--replace', required=False, default='REDACTED', help='word to replace with')
parser.add_argument('-t', '--threads', type=int, default=4, help='number of threads to use')
parser.add_argument('-s', '--slow', action='store_true', help='throttle performance')


@dataclass
class Replacer:

    find: str
    replace: str
    slow: bool

    def process_file(self, input_file: Path, output_file: Path):
        with logging_redirect_tqdm():
            logger.debug('Started "%s"', input_file)
            with input_file.open('r') as i:
                with output_file.open('w') as o:
                    for line in i:
                        o.write(line.replace(self.find, self.replace))
                        if self.slow:
                            time.sleep(random.random())
            logger.debug('Finished "%s"', input_file)


@chris_plugin(
    parser=parser,
    category='Text',
    title='Simple Find and Replace Utility',
    min_cpu_limit='2000m'
)
def main(options, inputdir: Path, outputdir: Path):

    mapper = PathMapper(inputdir, outputdir, glob=options.inputPathFilter)
    r = Replacer(find=options.find, replace=options.replace, slow=options.slow)

    with tqdm(desc='Processing', total=mapper.count()) as bar:

        def process_and_progress(i, o):
            r.process_file(i, o)
            bar.update()

        with ThreadPoolExecutor(max_workers=options.threads) as pool:
            print(f'Using {options.threads} threads')
            for input_file, output_file in mapper:
                pool.submit(process_and_progress, input_file, output_file)

        print('done')


if __name__ == '__main__':
    main()
