# How to Fix Black Formatting

Black is very strict about formatting and manual edits don't match its exact output.

## Solution: Run Black Directly

### Option 1: Using pipx (Recommended)
```bash
# Install pipx if needed
sudo apt install pipx

# Install black
pipx install black

# Format the file
~/.local/bin/black gitish/commands/show_issue.py --line-length=100

# Or format everything
~/.local/bin/black gitish/ tests/ --line-length=100
```

### Option 2: Using pip in virtual environment
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install black
pip install black

# Format files
black gitish/ tests/ --line-length=100

# Deactivate
deactivate
```

### Option 3: Use the script
```bash
./format_code.sh
```

## Then Commit
```bash
git add .
git commit -m "Fix: Apply Black formatting"
git push
```

## Why Manual Formatting Doesn't Work

Black has very specific rules about:
- Where to place spaces in multi-line strings
- How to break long lines
- Trailing commas
- Quote styles

The only way to guarantee Black compliance is to run Black itself.
