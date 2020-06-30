#!/bin/bash
set -exo pipefail

TESTS_REQUIREMENTS='tests/requirements.txt'

pip3 install --upgrade --requirement ${TESTS_REQUIREMENTS}

for FILE in "$@"; do
  pip3 install --upgrade --editable "$FILE"
done