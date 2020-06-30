#!/bin/bash
set -exo pipefail

usage() {
    echo "generate-and-sort-file [TEST_FILE_SIZE_MB] [CHANK_MAX_SIZE_MB]"
}

if [[ "$#" != 2 ]]; then
    usage
    exit 1
fi

TEST_FILE_SIZE_MB="$1"
CHANK_MAX_SIZE_MB="$2"

TEST_FILE_NAME="test_file"
OUTPUT_FILE="test_result"

TEST_FILE_SIZE=$((1024*1024*${TEST_FILE_SIZE_MB}))
CHANK_MAX_SIZE=$((1024*1024*${CHANK_MAX_SIZE_MB}))
MAX_WORD_LENGHT=30

file_generator.py --output_file $TEST_FILE_NAME --output_file_size $TEST_FILE_SIZE  --max_word_length $MAX_WORD_LENGHT
sorting_script.py --input_file $TEST_FILE_NAME --output_file $OUTPUT_FILE --chunk_max_size $CHANK_MAX_SIZE