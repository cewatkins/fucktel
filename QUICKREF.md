# Quick Reference Card - CP437 Telnet Client

## Project Setup (First Time)

```bash
cd /home/oo/src/fucktel
chmod +x setup_env.sh run_tests.sh
./setup_env.sh
```

## Daily Development

```bash
# Activate environment
source venv/bin/activate

# Run application
python3 cp437_telnet.py hostname [port]

# Run all tests
./run_tests.sh

# Or individual tests
python3 -m pytest tests/ -v
python3 -m unittest discover -s tests

# Deactivate when done
deactivate
```

## Code Quality Checks

```bash
# Format code
black cp437_telnet.py tests/

# All quality checks
flake8 cp437_telnet.py tests/
mypy cp437_telnet.py --ignore-missing-imports
coverage run -m pytest tests/ && coverage report -m
```

## Git & GitHub

```bash
# First time: Initialize git
git init
git add .
git commit -m "Initial commit: CP437 telnet client"
git remote add origin https://github.com/yourusername/cp437-telnet.git
git branch -M main
git push -u origin main

# Subsequent commits
git add .
git commit -m "Your message"
git push

# Create release
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

## Testing

```bash
# Unit tests
python3 -m unittest discover -s tests -p "test_*.py" -v

# Pytest
python3 -m pytest tests/ -v

# Coverage report
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report -m
coverage html  # Open htmlcov/index.html
```

## Pre-Submission Checklist

```bash
# Format
black cp437_telnet.py tests/

# Quality checks pass?
flake8 cp437_telnet.py tests/ && echo "✓ flake8 OK"
mypy cp437_telnet.py --ignore-missing-imports && echo "✓ mypy OK"

# Tests pass?
python3 -m pytest tests/ -v && echo "✓ tests OK"

# Files ready?
ls -la | grep -E "cp437_telnet|setup\.py|requirements|README|LICENSE|\.gitignore"

# Git ready?
git status  # Should show clean working directory
```

## Project Files

| File | Purpose |
|------|---------|
| `cp437_telnet.py` | Main application (async telnet client) |
| `tests/test_cp437.py` | Unit tests (16 test cases) |
| `setup.py` | Package configuration |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |
| `LICENSE` | MIT License |
| `.gitignore` | Git ignore rules |
| `.github/workflows/tests.yml` | CI/CD pipeline |
| `COMMANDS.md` | Detailed command reference |
| `setup_env.sh` | Automated setup script |
| `run_tests.sh` | Automated test runner |

## Key Features

✅ Full CP437 character support (256 characters)
✅ Async/await based non-blocking I/O
✅ CP437↔Unicode bidirectional encoding
✅ Interactive telnet terminal shell
✅ 16 comprehensive unit tests
✅ Black/flake8/mypy compliant code
✅ GitHub Actions CI/CD included
✅ Complete documentation

## Common Tasks

```bash
# Install in dev mode
pip install -e .

# Install specific dependencies
pip install telnetlib3

# Generate distribution
python3 setup.py sdist bdist_wheel

# Test connection
python3 cp437_telnet.py localhost 23

# Check test coverage
coverage html  # Then open htmlcov/index.html

# View git log
git log --oneline

# Check remote
git remote -v
```

## Emergency Fixes

```bash
# Reset venv
rm -rf venv && python3 -m venv venv && source venv/bin/activate

# Clear cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Reset git
git reset --hard HEAD

# Reinstall package
pip uninstall cp437-telnet -y && pip install -e .
```

## One-Line Verification

```bash
# Everything working?
black --check cp437_telnet.py tests/ && flake8 cp437_telnet.py tests/ && python3 -m pytest tests/ -v && echo "✓ ALL CHECKS PASSED"
```
