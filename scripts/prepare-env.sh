#!/bin/bash
set -exo pipefail

if [ ! -d "venv" ]; then
  echo "Creating python venv"
  python3 -m venv venv
else
  echo "venv already exist"
fi
