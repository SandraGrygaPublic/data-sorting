import os
import shutil

from pytest import fixture


@fixture(scope='session')
def temporary_directory_name():
    return 'tmp_test_dir'


@fixture(scope='session')
def directory_for_temporary_data(temporary_directory_name):
    try:
        os.mkdir(temporary_directory_name)
        print("Directory ", temporary_directory_name, " Created ")
    except FileExistsError:
        print("Directory ", temporary_directory_name, " already exists")

    yield temporary_directory_name

    shutil.rmtree(temporary_directory_name)
