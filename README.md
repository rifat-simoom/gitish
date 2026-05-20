# 🔍 Gitish

> **Find truly available open source issues** - Stop wasting time on issues someone is already working on

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![No Dependencies](https://img.shields.io/badge/dependencies-none-green.svg)]()
[![CI](https://github.com/rifat-simoom/gitish/workflows/CI/badge.svg)](https://github.com/rifat-simoom/gitish/actions)
[![codecov](https://codecov.io/gh/rifat-simoom/gitish/branch/main/graph/badge.svg)](https://codecov.io/gh/rifat-simoom/gitish)

## 🎯 The Problem

You find an interesting GitHub issue, spend time understanding it, start working on it... only to discover someone already submitted a PR. **Time wasted.**

## ✨ The Solution

This tool checks for **linked pull requests** and shows you only issues that are **truly available** to work on.

### What Makes This Unique?

- ✅ **Filters by Linked PRs** - No other tool does this
- ✅ **Beautiful Architecture** - Clean, organized, maintainable
- ✅ **Multi-Repository** - Works with any GitHub repository
- ✅ **Zero Dependencies** - Uses only Python stdlib
- ✅ **Smart Caching** - Respects GitHub rate limits
- ✅ **Professional CLI** - Well-structured commands

## 🚀 Quick Start

### Installation

#### From PyPI (Recommended)

```bash
pip install gitish
```

#### From Source

```bash
# Clone the repository
git clone https://github.com/rifat-simoom/gitish.git
cd gitish

# Install
pip install -e .
```

#### Development Installation

```bash
# Clone and install with dev dependencies
git clone https://github.com/rifat-simoom/gitish.git
cd gitish
pip install -e ".[dev]"
```

### Requirements

**Python 3.8+** - That's it! No other dependencies.

## 📖 Usage

### List Repositories

```bash
gitish list

# Output:
# 📋 Configured Repositories:
#   ✓ symfony     symfony/symfony
#     laravel     laravel/framework
#     react       facebook/react
#     ...17 repos total
```

### Find Available Issues

```bash
# Find available issues in Symfony
gitish available symfony

# Find bugs in Laravel
gitish available laravel --label=bug

# Find good first issues in React
gitish available react --label="good first issue"

# Use any repository (owner/repo format)
gitish available microsoft/TypeScript --label=bug
```

### View Issue Details

```bash
# See full issue with comments and linked PRs
gitish show 12345 symfony
```

## 🎨 Example Output

```
🔍 Fetching issues from symfony/symfony...
   Filtering by label: DX

✨ Found 2 available issues

  #62497  [Scheduler] [DX] Schedule's with() method is prone to w...
         Labels: DX, Scheduler
         Comments: 1  Updated: 2026-04-23

  #40794  [DX] Static vs. runtime env vars
         Labels: DX, Help wanted, Keep open
         Comments: 47  Updated: 2025-05-09

💡 Tips:
   • View details: gitish show <number> symfony
   • Filter: --label="bug" or --label="good first issue"
   • More results: --limit=50
```

## 🏗️ Project Structure

```
gitish/
├── gitish/                   # Main package
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration and settings
│   ├── cli.py                # CLI entry point
│   ├── commands/             # Command implementations
│   │   ├── __init__.py
│   │   ├── list_repos.py     # List repositories
│   │   ├── available_issues.py  # Find available issues
│   │   └── show_issue.py     # Show issue details
│   ├── services/             # Business logic
│   │   ├── __init__.py
│   │   └── github_api.py     # GitHub API client
│   └── utils/                # Utilities
│       ├── __init__.py
│       ├── repository.py     # Repository resolution
│       └── formatters.py     # Output formatting
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── conftest.py           # Pytest fixtures
│   ├── test_github_api.py    # API tests
│   ├── test_repository.py    # Repository tests
│   ├── test_formatters.py    # Formatter tests
│   └── test_cli.py           # CLI tests
├── .github/
│   └── workflows/            # GitHub Actions
│       ├── ci.yml            # CI pipeline
│       ├── publish.yml       # PyPI publishing
│       └── release.yml       # Release automation
├── pyproject.toml            # Modern Python packaging
├── setup.py                  # Setup script
├── Makefile                  # Development commands
├── README.md                 # This file
├── LICENSE                   # MIT License
└── CONTRIBUTING.md           # Contribution guidelines
```

### Architecture Highlights

- **Clean Separation** - Commands, services, and utilities are separate
- **Service Layer** - GitHub API interactions isolated in service
- **Command Pattern** - Each command is a separate class
- **Utilities** - Reusable formatters and helpers
- **No Dependencies** - Uses only Python standard library

## ⚙️ Configuration

### Built-in Repositories

Pre-configured with 17 popular projects:

**PHP**: Symfony, Laravel, PHPUnit, Doctrine, Guzzle  
**JavaScript**: React, Vue, Angular, Node.js, TypeScript  
**Python**: Django, Flask, pytest  
**Other**: Rust, Go, Rails, .NET

### Add Custom Repositories

Edit `gitish/config.py`:

```python
REPOSITORIES = {
    'myproject': 'username/repository',
    # ... existing repos
}
```

Or use `owner/repo` format directly:

```bash
gitish available username/repository
```

### GitHub Token (Recommended)

Increase rate limit from 60 to 5,000 requests/hour:

```bash
# Get token at: https://github.com/settings/tokens
export GITHUB_TOKEN="your_github_token_here"

# Add to ~/.bashrc or ~/.zshrc to persist
echo 'export GITHUB_TOKEN="your_github_token_here"' >> ~/.bashrc
```

**Note**: Token only needs read access (no scopes required)

## 🎓 How It Works

1. **Fetches Issues** - Uses GitHub API to get open issues
2. **Checks Timeline** - Examines timeline for cross-referenced PRs
3. **Filters Results** - Shows only issues without linked PRs
4. **Caches Data** - Stores in `~/.gitish/cache/` for 5 minutes

### Why This Matters

- **Saves Time** - No manual checking of each issue
- **Avoids Conflicts** - Don't work on issues with existing PRs
- **Better Success** - Focus on truly available issues
- **Clear Visibility** - See PR status at a glance

## 🤝 Contributing

Contributions welcome! This project has a clean architecture that's easy to extend.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/rifat-simoom/gitish.git
cd gitish

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Or use make
make install-dev
```

### Running Tests

```bash
# Run all tests with coverage
make test

# Or use pytest directly
pytest --cov=gitish --cov-report=term-missing
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Or run individually
black gitish tests
isort gitish tests
flake8 gitish tests
mypy gitish
```

### Development Commands

```bash
make help          # Show all available commands
make install       # Install package
make install-dev   # Install with dev dependencies
make test          # Run tests with coverage
make lint          # Run linters
make format        # Format code
make clean         # Remove build artifacts
make build         # Build distribution packages
```

### Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to all functions
- Keep functions small and focused
- Write tests for new features
- Format with Black (line length 100)
- Sort imports with isort

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📋 Roadmap

### Current (v1.0)
- ✅ Multi-repository support
- ✅ Linked PR detection
- ✅ Beautiful CLI interface
- ✅ Smart caching
- ✅ GitHub token support
- ✅ Clean architecture

### Planned (v2.0)
- [ ] Config file support (`~/.gitish.conf`)
- [ ] Colorized output with rich/colorama
- [ ] Progress indicators
- [ ] Watch for new issues
- [ ] Export to JSON/CSV
- [ ] Shell completion (bash/zsh)

### Future Ideas
- [ ] Web dashboard
- [ ] Browser extension
- [ ] IDE plugins
- [ ] Team collaboration features
- [ ] Contribution analytics

## 🎯 Use Cases

### For Contributors
- Quickly find available issues across multiple projects
- Avoid wasted effort on taken issues
- Discover good first issues
- Track multiple repositories easily

### For Maintainers
- Help contributors find available work
- Reduce duplicate PRs
- Improve contributor experience
- Share with your community

### For Teams
- Coordinate open source contributions
- Find issues matching team expertise
- Track contribution opportunities
- Encourage OSS participation

## 📊 Comparison

| Feature | This Tool | GitHub CLI | GitKraken | Others |
|---------|-----------|------------|-----------|--------|
| Filters by linked PRs | ✅ | ❌ | ❌ | ❌ |
| Clean architecture | ✅ | ✅ | ✅ | Varies |
| No dependencies | ✅ | ❌ | ❌ | ❌ |
| Multi-repo | ✅ | ✅ | ✅ | ✅ |
| Open source | ✅ | ✅ | ❌ | Varies |

## 🐛 Troubleshooting

### Rate Limit Errors

**Problem**: `403 rate limit exceeded`

**Solution**: Add GitHub token (see Configuration section)

### No Issues Found

**Possible reasons**:
- All issues have linked PRs (try different label)
- Repository has no open issues
- Network/API issues

**Solution**: Try different filters or repositories

### Import Errors

**Problem**: `ModuleNotFoundError`

**Solution**: 
```bash
# Install the package
pip install -e .

# Or run from project root
python -m gitish.cli list
```

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Built with Python standard library
- Powered by [GitHub API](https://docs.github.com/en/rest)
- Inspired by the need to contribute more effectively to open source

## 📞 Support

- 🐛 [Report Issues](https://github.com/rifat-simoom/gitish/issues)
- 💬 [Discussions](https://github.com/rifat-simoom/gitish/discussions)
- ⭐ Star the repo if this helps you!

## 🌟 Why This Project?

### The Story

While trying to contribute to Symfony, I kept finding "good first issues" that already had PRs in progress. After wasting hours on this, I built a tool to solve it. Now you can find truly available issues in seconds.

### The Impact

- **Saves Hours** - No more manual checking
- **Helps Thousands** - Any contributor can use this
- **Unique Solution** - No other tool filters by linked PRs
- **Beautiful Code** - Clean architecture, easy to maintain

---

**Made with ❤️ for the open source community**

*Stop wasting time on taken issues. Find truly available work in seconds.*

**Beautiful architecture. Zero dependencies. Just works.** 🎉
