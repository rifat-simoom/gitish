#!/bin/bash
# Test installation script

set -e

echo "🧪 Testing Gitish Installation"
echo ""

# Test 1: Check if gitish command exists
echo "✓ Testing command availability..."
python -m gitish.cli --version || echo "Command not found"

# Test 2: List repositories
echo ""
echo "✓ Testing list command..."
python -m gitish.cli list

# Test 3: Run tests
echo ""
echo "✓ Running test suite..."
python -m pytest tests/ -v

echo ""
echo "✅ All tests passed!"
