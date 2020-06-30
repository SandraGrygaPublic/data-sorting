import os

from file_generator import generate_test_file
from pytest import mark


@mark.parametrize('file_size, output_file_prefix', [
    (10, "file_to_sort_1"),
    (512, "file_to_sort_2"),
    (1024, "file_to_sort_3"),
    (1024 * 5, "file_to_sort_4"),
    (1024 * 1024, "file_to_sort_5"),
])
def test_if_file_size_is_correct(directory_for_temporary_data, file_size, output_file_prefix):
    file_name = os.path.join(directory_for_temporary_data, f"{output_file_prefix}")
    generate_test_file(file_name, file_size)

    assert os.path.exists(file_name)
    assert os.stat(file_name).st_size == file_size or os.stat(file_name).st_size == file_size + 1
