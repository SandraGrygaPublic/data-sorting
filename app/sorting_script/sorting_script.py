#!/usr/bin/python3

import os
from heapq import merge
from typing import List

import argparse


def sort_in_memory(unsorted_data: list):
    return sorted(unsorted_data, key=str.lower)


def get_data_chunk(file_name: str, chunk_max_size: int):
    with open(file_name) as file_with_data:
        data_to_load = os.stat(file_name).st_size
        while data_to_load > 0:
            loaded_data = []
            loaded_data_size = 0
            while data_to_load and loaded_data_size < chunk_max_size:
                loaded_word = file_with_data.readline()
                loaded_data.append(loaded_word)

                loaded_data_size += len(loaded_word)
                data_to_load -= len(loaded_word)
            yield loaded_data


def save_data(list_to_save: list, file_name: str):
    with open(file_name, 'w') as output_file:
        output_file.writelines(list_to_save)


def merge_sorted_files(temporary_files: List[str], output_file_name: str):
    sorted_files = []
    for file_name in temporary_files:
        sorted_files.append(open(file_name))

    with open(output_file_name, 'w') as output_file:
        output_file.writelines(merge(*sorted_files, key=lambda k: k.lower()))


def remove_temporary_files(temporary_files: List[str]):
    for file_name in temporary_files:
        os.remove(file_name)


def sort(file_name: str, output_file_name: str, chunk_max_size: int):
    temporary_files = []
    temporary_files_prefix = '.sorted_data_part'

    for data_to_sort in get_data_chunk(file_name, chunk_max_size):
        sorted_data = sort_in_memory(data_to_sort)
        temporary_file_name = f"{temporary_files_prefix}_{len(temporary_files)}"
        save_data(sorted_data, temporary_file_name)
        temporary_files.append(temporary_file_name)

    if len(temporary_files) == 1:
        os.rename(f"{temporary_files_prefix}_0", output_file_name)
    else:
        merge_sorted_files(temporary_files, output_file_name)
        remove_temporary_files(temporary_files)


def get_arguments():
    parser = argparse.ArgumentParser(description="Sort selected file")

    parser.add_argument("--input_file", action='store', help="Set input file", required=True)
    parser.add_argument("--output_file", action='store', help="Set output file", required=True)
    parser.add_argument("--chunk_max_size", action='store',
                        help="Set single load limit (How much data can be sort at once). Default value depends of avaible amound of RAM memory")

    return parser.parse_args()


if __name__ == "__main__":
    args = get_arguments()

    input_file_name = args.input_file
    output_file_name = args.output_file
    chunk_max_size = args.chunk_max_size

    if not chunk_max_size:
        chunk_max_size = 1024 * 1024 * 500  # TODO -> Should depend of system memory

    sort(input_file_name, output_file_name, int(chunk_max_size))
