# CP437 Telnet Client - Complete Setup & Submission Guide

## Quick Start

### 1. Initial Setup (One-time)

```bash
# Clone your repo (after pushing to GitHub)
git clone https://github.com/yourusername/cp437-telnet.git
cd cp437-telnet

# Make setup script executable
chmod +x setup_env.sh run_tests.sh

# Run setup
./setup_env.sh
```

### 2. Activate Environment (Each session)

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

### 3. Deactivate Environment (When done)

```bash
deactivate
```

---

## Essential Commands

### Installation & Setup

```bash
# Install dependencies only
pip install -r requirements.txt

# Install development dependencies
pip install pytest coverage flake8 black mypy

# Install package in editable/development mode
pip install -e .

# Uninstall package
pip uninstall cp437-telnet -y
```

### Running the Application

```bash
# Direct execution
python3 cp437_telnet.py hostname [port]

# Examples
python3 cp437_telnet.py bbs.example.com
python3 cp437_telnet.py localhost 6666
python3 cp437_telnet.py towel.blinkenlights.nl 23

# Via installed command (after `pip install -e .`)
cp437-telnet hostname
cp437-telnet hostname 6666
```

### Testing

```bash
# Run all tests (unittest)
python3 -m unittest discover -s tests -p "test_*.py" -v

# Run all tests (pytest)
python3 -m pytest tests/ -v

# Run specific test file
python3 -m unittest tests.test_cp437 -v

# Run specific test case
python3 -m unittest tests.test_cp437.TestCP437Decoding.test_decode_smiley_face -v

# Run tests with coverage
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report -m
coverage html  # Open htmlcov/index.html in browser

# Quick test run (automated script)
./run_tests.sh
```

### Code Quality

```bash
# Format code with Black
black cp437_telnet.py tests/

# Check formatting without modifying
black --check cp437_telnet.py tests/

# Lint with flake8
flake8 cp437_telnet.py tests/

# Type checking with mypy
mypy cp437_telnet.py --ignore-missing-imports

# Run all checks together
black --check cp437_telnet.py tests/ && \
flake8 cp437_telnet.py tests/ && \
mypy cp437_telnet.py --ignore-missing-imports && \
python3 -m pytest tests/ -v
```

### Building & Distribution

```bash
# Build source distribution
python3 setup.py sdist

# Build wheel distribution
python3 setup.py bdist_wheel

# Build both
python3 setup.py sdist bdist_wheel

# Clean build artifacts
python3 setup.py clean --all
rm -rf build/ dist/ *.egg-info

# Install from wheel (testing distribution)
pip install dist/cp437-telnet-*.whl
```

### Version Control & Git

```bash
# Initialize git repo (first time)
git init
git add .
git commit -m "Initial commit: CP437 telnet client"

# Add remote and push to GitHub
git remote add origin https://github.com/yourusername/cp437-telnet.git
git branch -M main
git push -u origin main

# Subsequent commits
git add .
git commit -m "Descriptive commit message"
git push

# Create a release tag
git tag -a v1.0.0 -m "Version 1.0.0 release"
git push origin v1.0.0
```

---

## Pre-GitHub Submission Checklist

### Code Quality

- [ ] `black --check cp437_telnet.py tests/` passes
- [ ] `flake8 cp437_telnet.py tests/` has no issues
- [ ] `mypy cp437_telnet.py --ignore-missing-imports` passes
- [ ] All tests pass: `python3 -m pytest tests/ -v`
- [ ] Coverage is >90%: `coverage report -m`

### Documentation

- [ ] README.md is complete and accurate
- [ ] Docstrings present in all functions
- [ ] Examples work as documented
- [ ] License file present (LICENSE)

### Project Structure

- [ ] .gitignore excludes `__pycache__`, `*.egg-info`, `dist/`, `build/`, `venv/`
- [ ] requirements.txt has correct dependencies
- [ ] setup.py is configured correctly
- [ ] .github/workflows/tests.yml exists for CI/CD

### Git Setup

- [ ] Initialize repo: `git init`
- [ ] Create .gitignore
- [ ] Commit all files: `git add . && git commit -m "Initial commit"`
- [ ] Add remote: `git remote add origin https://github.com/yourusername/cp437-telnet.git`
- [ ] Push to GitHub: `git push -u origin main`

---

## GitHub Repository Setup

### On GitHub Website

1. Create new repository at https://github.com/new
   - Name: `cp437-telnet`
   - Description: "A telnet client with CP437 graphical character support"
   - Public/Private: Public
   - Initialize: No (we'll push existing)
   - Add .gitignore: No (already have one)
   - Add license: No (already have LICENSE file)

2. After creation, follow the "push existing repository" instructions:

```bash
# From your local project directory
git remote add origin https://github.com/yourusername/cp437-telnet.git
git branch -M main
git push -u origin main
```

### Enable Features

- ✓ Discussions (optional)
- ✓ Projects (optional)
- ✓ Wiki (optional)
- ✓ GitHub Pages (optional - auto-generate from docs)

---

## Automation with GitHub Actions

The `.github/workflows/tests.yml` will automatically:
- Run tests on Python 3.8-3.12
- Check code formatting (black)
- Lint with flake8
- Run on Linux, macOS, and Windows
- Generate coverage reports

Trigger workflow by pushing to main branch or opening PRs.

---

## Complete Submission Flow

```bash
# 1. Setup (one time)
chmod +x setup_env.sh run_tests.sh
./setup_env.sh

# 2. Verify quality
./run_tests.sh

# 3. Format code
black cp437_telnet.py tests/

# 4. Final test
python3 -m pytest tests/ -v

# 5. Commit everything
git add .
git commit -m "Initial CP437 telnet client release"

# 6. Push to GitHub
git push origin main

# 7. Create release (optional)
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

---

## PyPI Publishing (Optional - Later)

When ready to publish to PyPI:

```bash
# Install twine
pip install twine

# Build distributions
python3 setup.py sdist bdist_wheel

# Upload to PyPI (requires credentials)
twine upload dist/*

# Or test on test.pypi.org first
twine upload --repository testpypi dist/*
```

---

## Troubleshooting

### Virtual Environment Issues

```bash
# If venv is corrupted
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Import Errors

```bash
# Ensure package is installed in development mode
pip install -e .

# Verify installation
python3 -c "import cp437_telnet; print(cp437_telnet.__file__)"
```

### Test Failures

```bash
# Run with more verbose output
python3 -m pytest tests/ -vv -s

# Run single test for debugging
python3 -m unittest tests.test_cp437.TestCP437Decoding -v
```

### Connection Issues During Testing

```bash
# Test locally first (doesn't connect to actual telnet server)
python3 -m pytest tests/ -v

# To test actual connection (requires telnet server)
python3 cp437_telnet.py localhost 23
```

---

## File Checklist

Before pushing, verify you have:

```bash
ls -la
# Should include:
# - cp437_telnet.py (main module)
# - setup.py (package config)
# - requirements.txt (dependencies)
# - README.md (documentation)
# - LICENSE (MIT license)
# - .gitignore (git ignore rules)
# - .github/workflows/tests.yml (CI/CD)
# - tests/test_cp437.py (unit tests)
# - setup_env.sh (setup script)
# - run_tests.sh (test script)
# - COMMANDS.md (this file)
```

---

## Resources

- [Telnetlib3 Docs](https://telnetlib3.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [CP437 Reference](https://en.wikipedia.org/wiki/Code_page_437)

---

## Support & Contribution

When others want to contribute:

```bash
# Fork the repo on GitHub
# Clone their fork
git clone https://github.com/theirusername/cp437-telnet.git

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes, test, commit
./run_tests.sh
git add .
git commit -m "Add amazing feature"

# Push and create Pull Request on GitHub
git push origin feature/amazing-feature
```

---

## Questions?

Refer to the main README.md for feature documentation and usage examples.
