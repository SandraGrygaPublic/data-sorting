#!/usr/bin/python3

import random
import string

import argparse


def generate_word(string_len: int):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in
                   range(string_len))


def generate_test_file(filename: str, data_to_generate: int, max_word_length: int = 12):
    with open(filename, 'w') as generated_file:
        while data_to_generate > 0:
            word_len = random.randint(1, max_word_length)
            if data_to_generate < max_word_length:  # length of the last word
                word_len = data_to_generate - 1  # one character is reserved for new line

            generated_file.write(f"{generate_word(word_len)}\n")
            data_to_generate -= word_len + 1


def get_arguments():
    parser = argparse.ArgumentParser(description="Test files generator")

    parser.add_argument("--output_file", action='store', help="Set output file", required=True)
    parser.add_argument("--output_file_size", action='store', help="Set output file size", required=True)
    parser.add_argument("--max_word_length", action='store', help="Set max word length")

    return parser.parse_args()


if __name__ == "__main__":
    args = get_arguments()

    output_file = args.output_file
    output_file_size = args.output_file_size
    max_word_length = args.max_word_length
    if not max_word_length:
        max_word_length = 12

    generate_test_file(output_file, int(output_file_size), int(max_word_length))
