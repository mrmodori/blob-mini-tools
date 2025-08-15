#!/usr/bin/env bash

# Exit on fail.
set -e

# Get the *real* path to this script, following symlinks.
SOURCE="$(realpath "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SOURCE")"

# Go to that directory.
cd "$SCRIPT_DIR/app"

# Run the Python app.
python3 main.py "$@"
