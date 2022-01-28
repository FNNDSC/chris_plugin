import shutil
from chris_plugin import chris_plugin, vectorize


@vectorize
def copy(input_file, output_file):
    print(f'Copying {input_file} to {output_file}')
    shutil.copyfile(input_file, output_file)


@chris_plugin
def main(_, inputdir, outputdir):
    print('Program started')
    copy(inputdir, outputdir)
    print('Complete!~')
