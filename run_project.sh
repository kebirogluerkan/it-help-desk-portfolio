#!/usr/bin/env bash
set -euo pipefail

python3 src/generate_data.py
python3 src/quality_check.py
python3 src/load_database.py
python3 src/analyze.py
python3 -m unittest discover -s tests -v
