#!/bin/bash
# Test runner script that uses .venv

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "Error: .venv directory not found. Please create it first:"
    echo "  python3 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -e ."
    exit 1
fi

# Use pytest from .venv
VENV_PYTEST=".venv/bin/pytest"

# Check if pytest is installed in .venv
if [ ! -f "$VENV_PYTEST" ]; then
    echo "Error: pytest not found in .venv. Installing dependencies..."
    .venv/bin/pip install -e ".[test]" 2>/dev/null || .venv/bin/pip install -e .
    .venv/bin/pip install pytest pytest-cov
fi

# Run pytest with all passed arguments
exec "$VENV_PYTEST" "$@"

