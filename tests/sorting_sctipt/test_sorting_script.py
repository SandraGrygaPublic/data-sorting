import os
from os import listdir
from os.path import isfile, join

from pytest import fixture, mark
from sorting_script import merge_sorted_files, sort, get_data_chunk, sort_in_memory


@fixture(scope='session')
def test_data_dir():
    return os.path.join('tests', "data")


def compare_results_from_file(name_of_generated_file, name_of_file_with_expected_result):
    with open(name_of_generated_file) as generated_file:
        with open(name_of_file_with_expected_result) as expectes_results_file:
            generated_data = [word.lower() for word in generated_file.readlines()]
            expectes_results = [word.lower() for word in expectes_results_file.readlines()]
            assert expectes_results == generated_data


@mark.parametrize('file_name', [
    "test_data_1",
    "test_data_2",
    "test_data_3",
])
def test_if_data_are_sorted_correctly(test_data_dir, file_name):
    input_file_name = os.path.join(test_data_dir, file_name)
    expected_result_file_name = f"{os.path.join(test_data_dir, file_name)}_expected_result"

    with open(input_file_name) as input_file:
        data_to_sort = [word.strip() for word in input_file.readlines()]
        with open(expected_result_file_name) as file_with_expected_result:
            expexted_result = [word.strip() for word in file_with_expected_result.readlines()]

            assert data_to_sort != expexted_result
            assert sort_in_memory(data_to_sort) == expexted_result


@mark.parametrize('file_name,single_load_limit,expected_temporary_files_number', [
    ("split_test", 100, 200),
    ("split_test", 1000, 20),
    ("split_test", 30000, 1),
])
def test_if_chunks_are_created_correctly(test_data_dir, file_name, single_load_limit, expected_temporary_files_number):
    input_file_name = os.path.join(test_data_dir, file_name)
    b = os.stat(input_file_name).st_size
    generated_chunks = list(get_data_chunk(input_file_name, single_load_limit))
    for chunk in generated_chunks:
        d = len(chunk)
    temporary_files_number = len(generated_chunks)
    assert temporary_files_number == expected_temporary_files_number


@mark.parametrize('temporary_files_number', [
    2,
    3,
    4,
])
def test_merging_function(directory_for_temporary_data, test_data_dir, temporary_files_number):
    output_file_name = os.path.join(directory_for_temporary_data, f'result_{temporary_files_number}')
    dir_path = os.path.join(test_data_dir, 'files_to_merge', f"{temporary_files_number}")
    expected_result_file = os.path.join(dir_path, 'expected_result')
    test_files = [join(dir_path, f) for f in listdir(dir_path) if isfile(join(dir_path, f)) and f != 'expected_result']

    merge_sorted_files(test_files, output_file_name)
    compare_results_from_file(expected_result_file, output_file_name)


@mark.parametrize('input_file_name, expected_result_file_name, chunk_max_size', [
    ('full_test_input', 'full_test_expected_result', 10),
    ('full_test_input', 'full_test_expected_result', 100),
    ('full_test_input', 'full_test_expected_result', 3000)
])
def test_all_sort_function(directory_for_temporary_data, test_data_dir, input_file_name, expected_result_file_name,
                           chunk_max_size):
    input_file_name = os.path.join(test_data_dir, input_file_name)
    output_file_name = os.path.join(directory_for_temporary_data, f'full_test_result')
    name_of_file_with_expected_result = os.path.join(test_data_dir, expected_result_file_name)

    sort(input_file_name, output_file_name, chunk_max_size)
    compare_results_from_file(output_file_name, name_of_file_with_expected_result)
