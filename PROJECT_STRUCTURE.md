# Gitish - Project Structure Documentation

## 📁 Complete Directory Structure

```
gitish/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Continuous Integration pipeline
│       ├── publish.yml         # PyPI publishing workflow
│       └── release.yml         # Release automation
│
├── gitish/                     # Main package
│   ├── __init__.py             # Package metadata
│   ├── config.py               # Configuration and settings
│   ├── cli.py                  # CLI entry point and argument parsing
│   │
│   ├── commands/               # Command implementations (Command Pattern)
│   │   ├── __init__.py
│   │   ├── list_repos.py       # List configured repositories
│   │   ├── available_issues.py # Find issues without linked PRs
│   │   └── show_issue.py       # Show detailed issue information
│   │
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   └── github_api.py       # GitHub API client with caching
│   │
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── repository.py       # Repository resolution and validation
│       └── formatters.py       # Output formatting utilities
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures and configuration
│   ├── test_github_api.py      # GitHub API service tests
│   ├── test_repository.py      # Repository utilities tests
│   ├── test_formatters.py      # Formatter utilities tests
│   └── test_cli.py             # CLI interface tests
│
├── .flake8                     # Flake8 linter configuration
├── .gitignore                  # Git ignore rules
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
├── Makefile                    # Development commands
├── MANIFEST.in                 # Package manifest
├── PROJECT_STRUCTURE.md        # This file
├── README.md                   # Main documentation
├── pyproject.toml              # Modern Python packaging config
├── requirements-dev.txt        # Development dependencies
├── setup.py                    # Setup script (uses pyproject.toml)
└── test_install.sh             # Installation test script
```

## 🏗️ Architecture Overview

### Layer Architecture

```
┌─────────────────────────────────────┐
│         CLI Layer (cli.py)          │  ← Entry point, argument parsing
├─────────────────────────────────────┤
│      Commands Layer (commands/)     │  ← Command implementations
├─────────────────────────────────────┤
│      Services Layer (services/)     │  ← Business logic, API calls
├─────────────────────────────────────┤
│      Utilities Layer (utils/)       │  ← Helper functions
└─────────────────────────────────────┘
```

### Design Patterns

1. **Command Pattern** - Each CLI command is a separate class
2. **Service Layer** - Business logic isolated from presentation
3. **Repository Pattern** - Repository resolution abstracted
4. **Strategy Pattern** - Different formatters for different outputs

## 📦 Package Components

### Core Package (`gitish/`)

#### `__init__.py`
- Package metadata (`__version__`, `__author__`, `__license__`)
- Package initialization

#### `config.py`
- Application settings (VERSION, APP_NAME)
- Cache configuration (CACHE_DIR, CACHE_TTL)
- GitHub API settings (GITHUB_API_BASE)
- Pre-configured repositories (REPOSITORIES dict)

#### `cli.py`
- CLI entry point (`main()` function)
- Argument parser creation
- Command routing
- Error handling

### Commands (`gitish/commands/`)

#### `list_repos.py`
- **Class**: `ListReposCommand`
- **Purpose**: Display all configured repositories
- **Output**: Formatted table with aliases and full names

#### `available_issues.py`
- **Class**: `AvailableIssuesCommand`
- **Purpose**: Find issues without linked PRs
- **Features**: Label filtering, result limiting, beautiful table output
- **Logic**: Fetches issues → Checks for linked PRs → Filters → Displays

#### `show_issue.py`
- **Class**: `ShowIssueCommand`
- **Purpose**: Display detailed issue information
- **Features**: Full description, comments, linked PRs, next steps

### Services (`gitish/services/`)

#### `github_api.py`
- **Class**: `GitHubAPI`
- **Purpose**: GitHub API client with caching
- **Features**:
  - Token authentication
  - Rate limit handling
  - File-based caching
  - Timeline parsing for linked PRs
- **Methods**:
  - `get_issues()` - Fetch issues list
  - `get_issue()` - Fetch single issue
  - `get_comments()` - Fetch issue comments
  - `get_timeline()` - Fetch issue timeline
  - `get_linked_prs()` - Extract linked PRs from timeline
  - `has_linked_prs()` - Check if issue has linked PRs

### Utilities (`gitish/utils/`)

#### `repository.py`
- **Functions**:
  - `resolve_repository()` - Resolve alias or owner/repo format
  - `get_repository_list()` - Get all configured repos
  - `get_default_repository()` - Get default repo
- **Exception**: `RepositoryError`

#### `formatters.py`
- **Functions**:
  - `truncate_text()` - Truncate text to fit
  - `format_table()` - Format data as table
  - `format_issue()` - Format issue for display
  - `format_pr_list()` - Format PR list
  - `format_labels()` - Format labels

## 🧪 Testing Structure

### Test Organization

```
tests/
├── conftest.py           # Shared fixtures
├── test_github_api.py    # API service tests
├── test_repository.py    # Repository utils tests
├── test_formatters.py    # Formatter tests
└── test_cli.py           # CLI tests
```

### Test Coverage

- **Unit Tests**: Individual functions and methods
- **Integration Tests**: Command execution flows
- **Mock Tests**: GitHub API calls (no real API calls in tests)

### Fixtures (`conftest.py`)

- `temp_cache_dir` - Temporary cache directory
- `mock_github_response` - Mock issue response
- `mock_issues_list` - Mock issues list

## 🔄 CI/CD Workflows

### CI Pipeline (`.github/workflows/ci.yml`)

**Triggers**: Push to main/develop, Pull requests

**Jobs**:
1. **Test** - Run on Python 3.6-3.12
   - Install dependencies
   - Lint with flake8
   - Format check with black
   - Import sort check with isort
   - Type check with mypy
   - Run pytest with coverage
   - Upload coverage to Codecov

2. **Lint** - Code quality checks
   - black, flake8, isort, mypy

### Publish Pipeline (`.github/workflows/publish.yml`)

**Trigger**: Release published

**Steps**:
1. Build package
2. Check with twine
3. Publish to PyPI

### Release Pipeline (`.github/workflows/release.yml`)

**Trigger**: Tag push (v*)

**Steps**:
1. Create GitHub release

## 📝 Configuration Files

### `pyproject.toml`
Modern Python packaging configuration:
- Build system requirements
- Project metadata
- Dependencies
- Entry points (`gitish` command)
- Tool configurations (black, isort, mypy, pytest, coverage)

### `.flake8`
Linter configuration:
- Line length: 100
- Ignored rules (compatible with black)
- Excluded directories

### `Makefile`
Development commands:
- `make install` - Install package
- `make install-dev` - Install with dev dependencies
- `make test` - Run tests
- `make lint` - Run linters
- `make format` - Format code
- `make clean` - Clean build artifacts
- `make build` - Build distribution
- `make publish` - Publish to PyPI

## 🚀 Development Workflow

### Setup
```bash
git clone https://github.com/rifat-simoom/gitish.git
cd gitish
pip install -e ".[dev]"
```

### Development Cycle
```bash
# 1. Make changes
vim gitish/commands/new_feature.py

# 2. Write tests
vim tests/test_new_feature.py

# 3. Run tests
make test

# 4. Format code
make format

# 5. Check linting
make lint

# 6. Commit
git commit -m "Add new feature"
```

### Release Process
```bash
# 1. Update version in pyproject.toml and __init__.py
# 2. Update CHANGELOG.md
# 3. Commit changes
# 4. Create tag
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0

# 5. GitHub Actions will:
#    - Create release
#    - Build package
#    - Publish to PyPI
```

## 📊 Code Metrics

### Package Size
- **Lines of Code**: ~1,500
- **Number of Files**: ~20
- **Test Coverage**: Target 80%+

### Dependencies
- **Runtime**: 0 (uses only Python stdlib)
- **Development**: 9 (pytest, black, flake8, etc.)

### Supported Python Versions
- Python 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12

## 🎯 Key Features

1. **Zero Runtime Dependencies** - Uses only Python standard library
2. **Beautiful Table Output** - Clean, formatted tables
3. **Smart Caching** - File-based caching with TTL
4. **Multi-Repository** - 17 pre-configured repos
5. **Linked PR Detection** - Unique feature
6. **Comprehensive Tests** - Full test coverage
7. **CI/CD Pipeline** - Automated testing and publishing
8. **Professional Structure** - Clean architecture

## 📚 Documentation

- **README.md** - User documentation
- **CONTRIBUTING.md** - Developer guidelines
- **PROJECT_STRUCTURE.md** - This file
- **Docstrings** - All functions documented
- **Type Hints** - Most functions typed

## 🔐 Security

- No secrets in code
- Token via environment variable
- Input validation
- HTTPS for API calls

## 🎨 Code Style

- **Formatter**: Black (line length 100)
- **Import Sorter**: isort
- **Linter**: flake8
- **Type Checker**: mypy
- **Style Guide**: PEP 8

---

**Last Updated**: 2026-05-20
**Version**: 1.0.0
