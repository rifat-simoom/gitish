#!/bin/bash
# Format all Python files with black and isort

echo "Installing formatters via pipx..."
pipx install black 2>/dev/null || echo "black already installed"
pipx install isort 2>/dev/null || echo "isort already installed"

echo "Sorting imports with isort..."
~/.local/bin/isort gitish/ tests/ --profile=black --line-length=100

echo "Formatting Python files with black..."
~/.local/bin/black gitish/ tests/ --line-length=100

echo "Done! Now fix remaining flake8 issues manually."
