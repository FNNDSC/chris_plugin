import subprocess as sp
from argparse import ArgumentParser
from chris_plugin import chris_plugin


parser = ArgumentParser(description='A ChRIS fs plugin wrapper for git clone')
parser.add_argument('-r', '--repo', required=True, type=str,
                    help='repository URI')


@chris_plugin(parser=parser, title='Git Clone')
def main(options, outputdir):
    sp.run(['git', 'clone', options.repo, outputdir], check=True)
