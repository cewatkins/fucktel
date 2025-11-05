#!/bin/bash
# CP437 Telnet Client - Setup and Testing Commands
# Run these commands to prepare your project for GitHub submission

set -e

echo "=================================================="
echo "CP437 Telnet Client - Environment Setup"
echo "=================================================="

# 1. Create and activate virtual environment
echo ""
echo "1. Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
echo "✓ Virtual environment created and activated"

# 2. Upgrade pip
echo ""
echo "2. Upgrading pip..."
pip install --upgrade pip setuptools wheel
echo "✓ pip upgraded"

# 3. Install dependencies
echo ""
echo "3. Installing project dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# 4. Install development tools
echo ""
echo "4. Installing development tools..."
pip install pytest coverage flake8 black mypy
echo "✓ Development tools installed"

# 5. Install in development mode
echo ""
echo "5. Installing package in development mode..."
pip install -e .
echo "✓ Package installed"

echo ""
echo "=================================================="
echo "Setup complete! Environment ready for development"
echo "=================================================="
