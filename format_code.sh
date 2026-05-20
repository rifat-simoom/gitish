#!/bin/bash
# Format all Python files with black

echo "Installing black via pipx..."
pipx install black 2>/dev/null || echo "black already installed"

echo "Formatting Python files..."
~/.local/bin/black gitish/ tests/ --line-length=100

echo "Done!"
