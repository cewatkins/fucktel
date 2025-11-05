#!/bin/bash
# CP437 Telnet Client - Testing Commands

set -e

source venv/bin/activate

echo "=================================================="
echo "Running Tests"
echo "=================================================="

echo ""
echo "1. Running unit tests with verbose output..."
python3 -m unittest discover -s tests -p "test_*.py" -v
echo "✓ Unit tests passed"

echo ""
echo "2. Running with pytest..."
python3 -m pytest tests/ -v
echo "✓ Pytest passed"

echo ""
echo "3. Checking code style with black..."
black --check cp437_telnet.py tests/
echo "✓ Code style check passed"

echo ""
echo "4. Linting with flake8..."
flake8 cp437_telnet.py tests/ --count --show-source
echo "✓ Flake8 linting passed"

echo ""
echo "5. Type checking with mypy..."
mypy cp437_telnet.py --ignore-missing-imports
echo "✓ Type checking passed"

echo ""
echo "6. Generating coverage report..."
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report -m
coverage html
echo "✓ Coverage report generated (see htmlcov/index.html)"

echo ""
echo "=================================================="
echo "All tests passed!"
echo "=================================================="
