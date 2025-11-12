#!/bin/bash
# Test script for C version of CP437 telnet client

set -e

echo "=========================================="
echo "CP437 Telnet Client - C Version Tests"
echo "=========================================="
echo ""

# Clean and build
echo "Building project..."
make clean
make all
echo "✓ Build successful"
echo ""

# Run examples
echo "Running examples (first 20 lines)..."
./examples_c | head -20
echo "... (output truncated)"
echo "✓ Examples run successfully"
echo ""

# Run tests
echo "Running unit tests..."
make test
echo ""

echo "=========================================="
echo "All tests completed successfully!"
echo "=========================================="
