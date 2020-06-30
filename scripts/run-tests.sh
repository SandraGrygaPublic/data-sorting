#!/bin/bash
set -euxo pipefail

pytest --cov=app --cov-config=.coveragerc --cov-report term-missing tests/
