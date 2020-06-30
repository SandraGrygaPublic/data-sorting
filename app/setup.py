import glob

from setuptools import setup, find_packages

setup(
    name='custom_sort',
    version='0.0.0',
    scripts=glob.glob('file_generator/file_generator.py') + glob.glob('sorting_script/sorting_script.py') + glob.glob(
        'scripts/generate-and-sort-file.sh'),
    packages=find_packages(),
    install_requires=[
    ],
)
